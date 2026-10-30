"""Talks to a local Ollama server (http://localhost:11434). No cloud, no API keys.
Any open-weight model works: llama3.2, qwen2.5, gemma2, mistral... set OFRENDA_MODEL."""
import json, os, urllib.request, urllib.error

HOST = lambda: os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
MODEL = lambda: os.environ.get("OFRENDA_MODEL", "llama3.2")
EMBED_MODEL = lambda: os.environ.get("OFRENDA_EMBED_MODEL", "nomic-embed-text")


def _post(path, payload, timeout=300):
    req = urllib.request.Request(HOST() + path, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.URLError as e:
        raise SystemExit(f"Can't reach Ollama at {HOST()} ({e.reason}).\n"
                         f"Install it from ollama.com, then: ollama pull {MODEL()}")


def chat(system: str, user: str, temperature=0.4) -> str:
    r = _post("/api/chat", dict(model=MODEL(), stream=False,
                                options=dict(temperature=temperature),
                                messages=[dict(role="system", content=system),
                                          dict(role="user", content=user)]))
    return r["message"]["content"].strip()


def embed(texts):
    """Returns list of vectors, or None if no embedding model is available (we fall back to keywords)."""
    try:
        return _post("/api/embed", dict(model=EMBED_MODEL(), input=texts), timeout=120)["embeddings"]
    except (SystemExit, KeyError):
        return None
