# -*- coding: utf-8 -*-
"""Ricerca carte su Scryfall con la sua sintassi completa. Pensato per il deck-building:
ordina per popolarita' EDHREC e mostra il prezzo indicativo EUR (Cardmarket trend).

Uso:
  python scripts/scryfall_search.py "o:proliferate id<=UBR"
  python scripts/scryfall_search.py "t:elf id<=BG cmc<=3" --limit 30
  python scripts/scryfall_search.py "o:\"whenever you discard\" id<=UBR" --max-eur 5
  python scripts/scryfall_search.py "is:commander id=WUR" --order edhrec

Sintassi utile: id<=BG (color identity), t:tipo, o:"testo oracle", cmc<=N,
is:commander, -is:reprint, usd/eur<=N. Docs: scryfall.com/docs/syntax
"""
import argparse
import json
import sys
import urllib.error

from ct_api import scryfall_get


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--order", default="edhrec", help="edhrec (default), eur, cmc, released...")
    ap.add_argument("--max-eur", type=float, default=None, help="filtra per prezzo massimo EUR")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    query = args.query + " game:paper"
    results, page_url = [], None
    try:
        res = scryfall_get("/cards/search", q=query, order=args.order, unique="cards")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"Nessuna carta trovata per: {args.query}")
        raise

    while True:
        for c in res.get("data", []):
            eur = c.get("prices", {}).get("eur")
            eur = float(eur) if eur else None
            if args.max_eur is not None and (eur is None or eur > args.max_eur):
                continue
            results.append({
                "name": c["name"],
                "mana_cost": c.get("mana_cost"),
                "type_line": c.get("type_line"),
                "color_identity": c.get("color_identity"),
                "eur": eur,
                "oracle_text": c.get("oracle_text"),
            })
            if len(results) >= args.limit:
                break
        if len(results) >= args.limit or not res.get("has_more"):
            break
        res = scryfall_get(res["next_page"].replace("https://api.scryfall.com", ""))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return
    print(f"{len(results)} risultati per: {args.query} (ordine: {args.order})")
    for r in results:
        eur = f"{r['eur']:7.2f} EUR" if r["eur"] is not None else "     ?  EUR"
        print(f"  {eur} | {r['name']:<35} | {r.get('mana_cost') or '':<10} | {r['type_line'][:40]}")


if __name__ == "__main__":
    main()
