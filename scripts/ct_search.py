# -*- coding: utf-8 -*-
"""Cerca le migliori offerte CardTrader per una carta, su tutte le sue stampe.

Uso:
  python scripts/ct_search.py "Heroic Intervention"
  python scripts/ct_search.py "Sol Ring" --lang en,it --top 10 --no-zero-only

Logica: stampe via Scryfall -> espansioni CardTrader (match per set code) ->
blueprint (match scryfall_id, fallback nome) -> offerte marketplace.
Ordina: prima venditori "X-Day Ready" (spediscono all'hub in giornata), poi prezzo.
Di default mostra solo offerte CardTrader Zero (spedizione consolidata).
Legge preferences.json (se esiste) per lingue/condizioni di default.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error

from ct_api import ct_get, scryfall_get, find_env

READY_RE = re.compile(r"\d+[\s-]?day[\s-]?ready", re.IGNORECASE)
CONDITION_ORDER = ["Mint", "Near Mint", "Slightly Played", "Moderately Played", "Played", "Poor"]

_expansions_cache = None


def load_preferences():
    env = find_env(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.dirname(env) if env else os.getcwd()
    p = os.path.join(root, "preferences.json")
    if os.path.isfile(p):
        return json.load(open(p, encoding="utf-8"))
    return {}


def ct_expansions_by_code():
    global _expansions_cache
    if _expansions_cache is None:
        _expansions_cache = {}
        for e in ct_get("/expansions"):
            if e["game_id"] == 1:  # Magic
                _expansions_cache.setdefault(e["code"].lower(), []).append(e)
    return _expansions_cache


def scryfall_prints(card_name):
    res = scryfall_get("/cards/search", q=f'!"{card_name}" game:paper', unique="prints", order="released")
    return res.get("data", [])


def search_offers(card_name, langs, zero_only=True, min_condition=None):
    prints = scryfall_prints(card_name)
    if not prints:
        return [], "carta non trovata su Scryfall"
    exact_name = prints[0]["name"]
    set_codes = list(dict.fromkeys(p["set"] for p in prints))
    scryfall_ids = {p["id"] for p in prints}
    exp_map = ct_expansions_by_code()

    allowed_conditions = None
    if min_condition and min_condition in CONDITION_ORDER:
        allowed_conditions = set(CONDITION_ORDER[:CONDITION_ORDER.index(min_condition) + 1])

    offers = []
    for code in set_codes:
        for exp in exp_map.get(code, []):
            try:
                bps = ct_get("/blueprints/export", expansion_id=exp["id"])
            except urllib.error.HTTPError:
                continue
            matches = [b for b in bps if b.get("scryfall_id") in scryfall_ids] or \
                      [b for b in bps if (b.get("name") or "").lower() == exact_name.lower()]
            for bp in matches:
                try:
                    prods = ct_get("/marketplace/products", blueprint_id=bp["id"])
                except urllib.error.HTTPError:
                    continue
                for o in prods.get(str(bp["id"]), []):
                    props = o.get("properties_hash", {})
                    if props.get("mtg_language") not in langs:
                        continue
                    if zero_only and not o["user"].get("can_sell_via_hub"):
                        continue
                    if allowed_conditions and props.get("condition") not in allowed_conditions:
                        continue
                    ready = READY_RE.search(o["user"]["username"])
                    offers.append({
                        "product_id": o["id"],
                        "name": exact_name,
                        "price_eur": o["price_cents"] / 100,
                        "condition": props.get("condition"),
                        "lang": props.get("mtg_language"),
                        "foil": props.get("mtg_foil"),
                        "expansion": exp["name"],
                        "seller": o["user"]["username"],
                        "country": o["user"]["country_code"],
                        "ct_zero": bool(o["user"].get("can_sell_via_hub")),
                        "fast": ready.group(0) if ready else None,
                        "qty": o["quantity"],
                    })
            time.sleep(0.05)
    offers.sort(key=lambda x: (x["fast"] is None, x["price_eur"]))
    return offers, None


def main():
    prefs = load_preferences()
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--lang", default=",".join(prefs.get("languages", ["en", "it"])))
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-condition", default=prefs.get("min_condition"))
    ap.add_argument("--no-zero-only", action="store_true", help="includi anche venditori senza CardTrader Zero")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    langs = [l.strip() for l in args.lang.split(",")]
    offers, err = search_offers(args.card, langs, zero_only=not args.no_zero_only,
                                min_condition=args.min_condition)
    if err:
        sys.exit(f"ERRORE: {err}")

    top = offers[:args.top]
    if args.json:
        print(json.dumps(top, ensure_ascii=False, indent=1))
        return
    print(f"{args.card}: {len(offers)} offerte trovate (lingue {langs}, "
          f"{'solo CT Zero' if not args.no_zero_only else 'tutti i venditori'})")
    for o in top:
        tag = f" [{o['fast']}]" if o["fast"] else ""
        foil = " FOIL" if o["foil"] else ""
        print(f"  {o['price_eur']:7.2f} EUR | {o['condition']:<18} | {o['lang']} | "
              f"{o['expansion'][:28]:<28} | {o['seller'][:26]:<26} ({o['country']}) "
              f"| id {o['product_id']}{tag}{foil}")


if __name__ == "__main__":
    main()
