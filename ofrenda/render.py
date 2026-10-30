"""One self-contained HTML file: no CDN, no fonts, no trackers. Works offline, forever."""
import base64, html, mimetypes
from . import store

CSS = """
:root{--bg:#120b14;--ink:#f6e7cf;--gold:#f5a623;--org:#e8710a;--violet:#6b3fa0;--pink:#d6336c}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#2a1533,var(--bg) 70%);
color:var(--ink);font-family:Georgia,'Times New Roman',serif;line-height:1.6;min-height:100vh}
header{text-align:center;padding:3rem 1rem 1rem}h1{font-size:2.6rem;margin:.2rem;letter-spacing:.08em;color:var(--gold)}
.sub{opacity:.7;font-style:italic}
.papel{height:34px;margin:1rem auto;max-width:900px;background:repeating-linear-gradient(90deg,
var(--pink) 0 40px,var(--gold) 40px 80px,var(--violet) 80px 120px,var(--org) 120px 160px);
clip-path:polygon(0 0,100% 0,100% 40%,97% 100%,94% 40%,91% 100%,88% 40%,85% 100%,82% 40%,79% 100%,76% 40%,73% 100%,70% 40%,67% 100%,64% 40%,61% 100%,58% 40%,55% 100%,52% 40%,49% 100%,46% 40%,43% 100%,40% 40%,37% 100%,34% 40%,31% 100%,28% 40%,25% 100%,22% 40%,19% 100%,16% 40%,13% 100%,10% 40%,7% 100%,4% 40%,1% 100%,0 40%);opacity:.85}
main{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:1.6rem;padding:1.5rem;max-width:1200px;margin:auto}
.card{background:rgba(255,255,255,.05);border:1px solid rgba(245,166,35,.35);border-radius:14px;padding:1.4rem;
box-shadow:0 0 30px rgba(245,166,35,.08);position:relative}
.photo{width:130px;height:160px;object-fit:cover;border:6px solid var(--gold);border-radius:4px;display:block;margin:0 auto 1rem;
filter:sepia(.25)}.nophoto{display:flex;align-items:center;justify-content:center;font-size:3rem;background:#2a1533}
h2{text-align:center;margin:.2rem 0;color:var(--gold)}.years{text-align:center;opacity:.7;margin-bottom:1rem}
.rem{white-space:pre-wrap;font-size:1.02rem}
.cempa{display:flex;justify-content:center;gap:.35rem;margin:.9rem 0}
.cempa i{width:22px;height:22px;border-radius:50%;background:radial-gradient(circle,#ffd45e 0 25%,var(--org) 26% 60%,#b3470a 61%);
box-shadow:0 0 8px #f5a62388}
.lists{display:grid;gap:.5rem;font-size:.95rem;margin-top:1rem}.lists b{color:var(--gold)}
details{margin-top:1rem;border-top:1px solid rgba(255,255,255,.12);padding-top:.7rem}summary{cursor:pointer;color:var(--gold)}
blockquote{margin:.7rem 0;padding-left:.8rem;border-left:3px solid var(--org);font-size:.95rem}
.candle{position:absolute;top:-18px;right:18px;width:12px;height:42px;background:linear-gradient(#fff6dc,#e9d3a0);border-radius:2px}
.candle:before{content:"";position:absolute;left:1px;top:-20px;width:10px;height:20px;border-radius:50% 50% 50% 50%/70% 70% 30% 30%;
background:radial-gradient(#fff 10%,#ffd45e 40%,var(--org));filter:drop-shadow(0 0 10px #f5a623);animation:fl 1.6s infinite alternate ease-in-out}
@keyframes fl{0%{transform:scale(1,1) rotate(-2deg);opacity:.9}50%{transform:scale(.92,1.1) rotate(2deg)}100%{transform:scale(1.05,.95) rotate(-1deg);opacity:1}}
footer{text-align:center;opacity:.5;padding:2rem;font-size:.85rem}
@media(prefers-reduced-motion:reduce){.candle:before{animation:none}}
@media print{body{background:#fff;color:#000}.card{break-inside:avoid;box-shadow:none}.candle,.papel{display:none}}
"""


def _photo(p):
    path = store.photo_path(p)
    if not path or not path.exists():
        return '<div class="photo nophoto" aria-hidden="true">🕯️</div>'
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f'<img class="photo" alt="Photo of {html.escape(p["name"])}" src="data:{mime};base64,{b64}">'


def _list(label, vals):
    return f"<div><b>{label}:</b> {html.escape(', '.join(vals))}</div>" if vals else ""


def card(p):
    e = html.escape
    yrs = " – ".join(x for x in (p.get("born"), p.get("died")) if x)
    ss = store.stories(p["slug"])
    stories = ""
    if ss:
        qs = "".join(f"<blockquote>{e(s['text'])}"
                     f"{' — ' + e(s['teller']) if s.get('teller') else ''}</blockquote>" for s in ss)
        stories = f"<details><summary>Stories ({len(ss)})</summary>{qs}</details>"
    rem = e(p.get("remembrance") or "")
    return (f'<section class="card"><div class="candle"></div>{_photo(p)}<h2>{e(p["name"])}</h2>'
            f'<div class="years">{e(yrs)}</div><div class="rem">{rem}</div><div class="cempa">{"<i></i>"*5}</div>'
            f'<div class="lists">{_list("Favorite foods", p.get("foods"))}{_list("Songs", p.get("songs"))}'
            f'{_list("Cherished things", p.get("items"))}</div>{stories}</section>')


def build(title="Ofrenda", out="ofrenda.html"):
    people = store.list_people()
    body = "\n".join(card(p) for p in people) or "<p style='text-align:center'>Add someone to begin.</p>"
    doc = (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{html.escape(title)}</title><style>{CSS}</style><header><h1>{html.escape(title)}</h1>'
           f'<div class="sub">Mientras los recordemos, siguen con nosotros.</div></header><div class="papel"></div>'
           f'<main>{body}</main><footer>Made locally, offline, with open-weight models. Nothing left this machine.</footer></html>')
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out
