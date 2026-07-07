# -*- coding: utf-8 -*-
"""Testo ufficiale + ruling ufficiali di una carta (via Scryfall).

Uso:
  python scripts/card_rulings.py "Lathril, Blade of the Elves"
  python scripts/card_rulings.py "putrificare"     (funzionano anche i nomi italiani)
"""
import sys
import urllib.error

from ct_api import scryfall_get


def find_card(name):
    for mode in ("exact", "fuzzy"):
        try:
            return scryfall_get("/cards/named", **{mode: name})
        except urllib.error.HTTPError:
            continue
    try:
        res = scryfall_get("/cards/search", q=f'lang:it "{name}"', unique="cards")
        if res.get("data"):
            return res["data"][0]
    except urllib.error.HTTPError:
        pass
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    c = find_card(name)
    if not c:
        sys.exit(f"Carta non trovata: {name}")

    print(f"=== {c['name']}" + (f" ({c.get('printed_name')})" if c.get("printed_name") else "") + " ===")
    print(f"{c.get('mana_cost') or ''}  {c.get('type_line')}")
    print(c.get("oracle_text") or "")
    if c.get("power") is not None:
        print(f"{c['power']}/{c['toughness']}")
    if c.get("loyalty") is not None:
        print(f"Fedelta': {c['loyalty']}")

    rulings = scryfall_get(f"/cards/{c['id']}/rulings")
    data = rulings.get("data", [])
    print(f"\n--- Ruling ufficiali ({len(data)}) ---")
    for r in data:
        print(f"[{r['published_at']}] {r['comment']}")
    if not data:
        print("(nessun ruling pubblicato per questa carta)")


if __name__ == "__main__":
    main()
