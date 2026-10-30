"""Grounded remembrance + Q&A. The rule: the model may only use what the family actually said."""
import math, re
from . import llm, store

REMEMBER_SYS = (
    "You help a family write a remembrance for a loved one who has died, for their ofrenda. "
    "Use ONLY facts found in the details and stories provided. NEVER invent names, dates, places, "
    "or events. If little is known, write less. Warm, plain, specific, 120-180 words, written as "
    "a family member speaking. Write in the same language as the stories. Output only the text."
)
ASK_SYS = (
    "You answer questions about a loved one using ONLY the numbered story excerpts provided. "
    "Cite the excerpts you used like [2]. If the answer is not in the excerpts, say plainly that "
    "the family hasn't recorded that yet, and suggest asking a relative. Never guess. "
    "Reply in the language of the question."
)


def _facts(p):
    lines = [f"Name: {p['name']}"]
    for k, label in (("born", "Born"), ("died", "Died")):
        if p.get(k): lines.append(f"{label}: {p[k]}")
    for k, label in (("foods", "Favorite foods"), ("songs", "Favorite songs"), ("items", "Cherished items")):
        if p.get(k): lines.append(f"{label}: {', '.join(p[k])}")
    return "\n".join(lines)


def remember(slug):
    p = store.get_person(slug)
    ss = store.stories(slug)
    body = _facts(p) + "\n\nStories:\n" + ("\n".join(f"[{s['id']}] {s['text']}" for s in ss) or "(none yet)")
    p["remembrance"] = llm.chat(REMEMBER_SYS, body, temperature=0.5)
    store.save_person(p)
    return p["remembrance"]


def _tok(t):
    return set(re.findall(r"\w{3,}", t.lower()))


def _cos(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else 0.0


def retrieve(slug, question, k=4):
    ss = store.stories(slug)
    if not ss:
        return []
    vecs = llm.embed([question] + [s["text"] for s in ss])
    if vecs:
        q, rest = vecs[0], vecs[1:]
        scored = [(_cos(q, v), s) for v, s in zip(rest, ss)]
    else:  # keyword fallback: still works with only a chat model installed
        qt = _tok(question)
        scored = [(len(qt & _tok(s["text"])) / (1 + len(qt)), s) for s in ss]
    return [s for _, s in sorted(scored, key=lambda x: -x[0])[:k]]


def ask(slug, question):
    p = store.get_person(slug)
    ctx = retrieve(slug, question)
    if not ctx:
        return "No stories have been recorded for them yet."
    body = _facts(p) + "\n\nExcerpts:\n" + "\n".join(f"[{s['id']}] {s['text']}" for s in ctx) \
           + f"\n\nQuestion: {question}"
    return llm.chat(ASK_SYS, body, temperature=0.2)
