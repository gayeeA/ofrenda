# 🕯️ Ofrenda — a private, offline ofrenda & oral-history keeper

*Ghost in the Machine* entry. Record a loved one's stories, let a **local open-weight model** help write
their remembrance, ask questions that are answered **only from what your family actually said**, and
render a candlelit, single-file HTML ofrenda that works offline forever.

## Quick start
```bash
# 1. Open pieces (all free, all local)
#    Ollama: https://ollama.com
ollama pull llama3.2            # any open-weight chat model works (qwen2.5, gemma2, mistral...)
ollama pull nomic-embed-text    # optional: better story search (keyword fallback otherwise)
pip install -r requirements.txt # optional: faster-whisper for audio

# 2. Use it
python -m ofrenda add "Abuela Rosa" --born 1931 --died 2019 \
    --foods "tamales,champurrado" --songs "Cielito Lindo" --items "blue rebozo" --photo rosa.jpg
python -m ofrenda story abuela-rosa --audio grandma_kitchen.m4a --teller "Mamá" --language es
python -m ofrenda story abuela-rosa --text "Every December she sang while stirring the masa."
python -m ofrenda remember abuela-rosa
python -m ofrenda ask abuela-rosa "What did she cook at Christmas?"
python -m ofrenda build --title "Ofrenda de la familia García"   # -> ofrenda.html
```
Data lives in plain JSON under `./ofrenda_data` (change with `OFRENDA_HOME`). Env vars:
`OFRENDA_MODEL`, `OFRENDA_EMBED_MODEL`, `OFRENDA_WHISPER` (tiny/small/medium), `OLLAMA_HOST`.

Run tests: `python -m unittest discover -s tests`

## Design choices
- **Grounded, not hallucinated.** The remembrance and Q&A prompts forbid inventing facts; if the answer isn't in a
  story, the model says the family hasn't recorded it. Grief is the wrong place for confident fiction.
- **Zero runtime dependencies** in the core (stdlib only). Whisper is optional.
- **Output is one HTML file** with inline CSS, no CDN, no fonts, no JS, no trackers. Escaped against injection.
- **Bilingual:** models reply in the language of the stories/question (try Spanish, Telugu, Hindi...).

## Post draft: why open matters here
Family recordings are about the most private data a person owns: a grandmother's voice, names, illnesses,
old grudges. With Ofrenda, **Whisper transcribes on-device, the LLM runs on-device, and nothing is uploaded.**
It works on a laptop with the Wi-Fi off, costs nothing per story, and I can swap `llama3.2` for any other
open-weight model, or a Spanish-tuned one, with one env var. The data is plain JSON and the output is plain HTML,
so the memorial can't vanish when a startup shuts down or changes its pricing. Closed APIs would mean sending a
loved one's voice to a server I don't control, for a tool meant to outlast me.
