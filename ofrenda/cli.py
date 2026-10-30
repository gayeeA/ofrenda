import argparse, sys
from pathlib import Path
from . import store, memory, render


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ofrenda", description="A private, offline ofrenda & oral-history keeper.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add a loved one")
    a.add_argument("name"); a.add_argument("--born", default=""); a.add_argument("--died", default="")
    a.add_argument("--foods", default=""); a.add_argument("--songs", default=""); a.add_argument("--items", default="")
    a.add_argument("--photo")

    s = sub.add_parser("story", help="add a story (typed, from a text file, or a recording)")
    s.add_argument("slug"); g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--text"); g.add_argument("--text-file"); g.add_argument("--audio")
    s.add_argument("--teller", default=""); s.add_argument("--language", default=None, help="e.g. es, en (auto if omitted)")

    r = sub.add_parser("remember", help="write a remembrance grounded in the stories"); r.add_argument("slug")
    q = sub.add_parser("ask", help="ask about them; answers only from recorded stories")
    q.add_argument("slug"); q.add_argument("question")
    sub.add_parser("people", help="list everyone")
    b = sub.add_parser("build", help="render the offline HTML ofrenda")
    b.add_argument("--title", default="Ofrenda"); b.add_argument("--out", default="ofrenda.html")

    n = ap.parse_args(argv)
    csv = lambda v: [x.strip() for x in v.split(",") if x.strip()]

    if n.cmd == "add":
        p = store.add_person(n.name, n.born, n.died, csv(n.foods), csv(n.songs), csv(n.items), n.photo)
        print(f"🕯️  Added {p['name']} (id: {p['slug']})")
    elif n.cmd == "story":
        if n.audio:
            from .transcribe import transcribe
            text, src = transcribe(n.audio, n.language), f"audio:{Path(n.audio).name}"
            print("\n--- transcript (edit stories.json to fix errors) ---\n" + text + "\n")
        elif n.text_file:
            text, src = Path(n.text_file).read_text("utf-8"), f"file:{Path(n.text_file).name}"
        else:
            text, src = n.text, "typed"
        st = store.add_story(n.slug, text, src, n.teller)
        print(f"📖 Saved story #{st['id']}")
    elif n.cmd == "remember":
        print(memory.remember(n.slug))
    elif n.cmd == "ask":
        print(memory.ask(n.slug, n.question))
    elif n.cmd == "people":
        for p in store.list_people():
            print(f"{p['slug']:24} {p['name']}  ({len(store.stories(p['slug']))} stories)")
    elif n.cmd == "build":
        print(f"✨ Wrote {render.build(n.title, n.out)}  — open it in any browser, even offline.")


if __name__ == "__main__":
    sys.exit(main())
