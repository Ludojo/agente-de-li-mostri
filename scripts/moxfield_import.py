# -*- coding: utf-8 -*-
"""Importa un mazzo da un link Moxfield e lo stampa in JSON (commander, lands, spells).

Uso:
  python scripts/moxfield_import.py https://moxfield.com/decks/vi4X68scA0GECQ2tXcKTPg
  python scripts/moxfield_import.py vi4X68scA0GECQ2tXcKTPg
"""
import json
import re
import sys
import urllib.request

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

USER_AGENT = "AgenteDeLiMostri/1.0"


def deck_id(arg):
    m = re.search(r"moxfield\.com/decks/([A-Za-z0-9_-]+)", arg)
    return m.group(1) if m else arg


def fetch(public_id):
    url = f"https://api2.moxfield.com/v2/decks/all/{public_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = fetch(deck_id(sys.argv[1]))

    commanders = [v["card"]["name"] for v in d.get("commanders", {}).values()]
    lands, spells = [], []
    for v in d.get("mainboard", {}).values():
        c = v["card"]
        entry = {
            "name": c["name"],
            "quantity": v["quantity"],
            "mana_cost": c.get("mana_cost"),
            "cmc": c.get("cmc"),
            "type_line": c.get("type_line"),
            "color_identity": c.get("color_identity"),
            "oracle_text": c.get("oracle_text"),
            "scryfall_id": c.get("scryfall_id"),
        }
        (lands if "Land" in (c.get("type_line") or "") else spells).append(entry)

    total = sum(x["quantity"] for x in lands + spells) + len(commanders)
    out = {
        "name": d.get("name"),
        "source": d.get("publicUrl"),
        "format": d.get("format"),
        "commanders": commanders,
        "lands": lands,
        "spells": spells,
        "total_cards": total,
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if d.get("format") == "commander" and total != 100:
        print(f"\nATTENZIONE: il mazzo ha {total} carte, non 100 — segnalalo all'utente.", file=sys.stderr)


if __name__ == "__main__":
    main()
