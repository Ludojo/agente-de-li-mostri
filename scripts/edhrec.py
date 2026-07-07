# -*- coding: utf-8 -*-
"""Statistiche EDHREC per un comandante: carte piu' giocate per categoria con % di inclusione.

Uso:
  python scripts/edhrec.py "Lathril, Blade of the Elves"
  python scripts/edhrec.py "Lathril, Blade of the Elves" --json
"""
import json
import re
import sys
import unicodedata
import urllib.request

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

USER_AGENT = "AgenteDeLiMostri/1.0"


def slugify(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower().replace("'", "")
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return name


def fetch(commander):
    slug = slugify(commander)
    url = f"https://json.edhrec.com/pages/commanders/{slug}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python scripts/edhrec.py \"<nome comandante>\" [--json]")
    commander = sys.argv[1]
    as_json = "--json" in sys.argv

    data = fetch(commander)
    container = data.get("container", {}).get("json_dict", {})
    cardlists = container.get("cardlists", [])

    out = {}
    for cl in cardlists:
        cat = cl.get("header", cl.get("tag", "?"))
        cards = []
        for cv in cl.get("cardviews", []):
            cards.append({
                "name": cv.get("name"),
                "inclusion_pct": round(100 * cv.get("num_decks", 0) / max(cv.get("potential_decks", 1), 1)),
                "num_decks": cv.get("num_decks"),
                "synergy": cv.get("synergy"),
            })
        out[cat] = cards

    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    total = data.get("container", {}).get("json_dict", {}).get("card", {})
    print(f"EDHREC — {commander}")
    for cat, cards in out.items():
        print(f"\n== {cat} ==")
        for c in cards[:15]:
            syn = f" | synergy {c['synergy']:+.0%}" if isinstance(c.get("synergy"), (int, float)) else ""
            print(f"  {c['inclusion_pct']:3d}% | {c['name']}{syn}")


if __name__ == "__main__":
    main()
