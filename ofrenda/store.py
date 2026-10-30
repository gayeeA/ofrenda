"""Plain-JSON storage. Everything lives in one folder you own: copy it, back it up, read it in 50 years."""
import json, os, re, time, unicodedata
from pathlib import Path


def home() -> Path:
    p = Path(os.environ.get("OFRENDA_HOME", "./ofrenda_data")).expanduser()
    (p / "people").mkdir(parents=True, exist_ok=True)
    return p


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "person"


def _dir(slug):
    return home() / "people" / slug


def _read(path, default):
    return json.loads(path.read_text("utf-8")) if path.exists() else default


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), "utf-8")


def add_person(name, born="", died="", foods=(), songs=(), items=(), photo=None):
    slug = slugify(name)
    d = _dir(slug)
    person = _read(d / "person.json", {})
    person.update(name=name, slug=slug, born=born or person.get("born", ""),
                  died=died or person.get("died", ""),
                  foods=list(foods) or person.get("foods", []),
                  songs=list(songs) or person.get("songs", []),
                  items=list(items) or person.get("items", []),
                  remembrance=person.get("remembrance", ""))
    if photo:
        import shutil
        dest = d / ("photo" + Path(photo).suffix.lower())
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(photo, dest)
        person["photo"] = dest.name
    _write(d / "person.json", person)
    return person


def get_person(slug):
    p = _read(_dir(slug) / "person.json", None)
    if p is None:
        raise SystemExit(f"No such person '{slug}'. Run `ofrenda people`.")
    return p


def save_person(person):
    _write(_dir(person["slug"]) / "person.json", person)


def list_people():
    out = []
    for f in sorted((home() / "people").glob("*/person.json")):
        out.append(json.loads(f.read_text("utf-8")))
    return out


def stories(slug):
    return _read(_dir(slug) / "stories.json", [])


def add_story(slug, text, source="typed", teller=""):
    get_person(slug)
    items = stories(slug)
    item = dict(id=len(items) + 1, text=text.strip(), source=source, teller=teller,
                added=time.strftime("%Y-%m-%d"))
    items.append(item)
    _write(_dir(slug) / "stories.json", items)
    return item


def save_stories(slug, items):
    _write(_dir(slug) / "stories.json", items)


def photo_path(person):
    return _dir(person["slug"]) / person["photo"] if person.get("photo") else None
