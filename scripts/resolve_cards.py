# -*- coding: utf-8 -*-
"""Risolve una lista di carte (nomi EN o IT, anche con refusi) in carte Scryfall esatte.

Uso:
  python scripts/resolve_cards.py lista.txt
  python scripts/resolve_cards.py -            (legge da stdin)

Formato input: una carta per riga, opzionale quantita' iniziale ("4 Foresta", "1 sol ring", "putrificare").
Output: JSON su stdout con carte risolte + elenco AMBIGUE/NON TROVATE su stderr.
"""
import json
import re
import sys
import urllib.error

from ct_api import scryfall_get

QTY_RE = re.compile(r"^\s*(\d+)\s*[xX]?\s+(.\S*.*)$")


def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    m = QTY_RE.match(line)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return 1, line


def try_named(name):
    for mode in ("exact", "fuzzy"):
        try:
            c = scryfall_get("/cards/named", **{mode: name})
            return c, mode
        except urllib.error.HTTPError:
            continue
    return None, None


def try_italian(name):
    """Cerca per nome stampato italiano, prima esatto poi per parole chiave."""
    try:
        res = scryfall_get("/cards/search", q=f'lang:it "{name}"', unique="cards")
        if res.get("data"):
            return res["data"], "it-exact"
    except urllib.error.HTTPError:
        pass
    words = [w for w in re.findall(r"[a-zà-ù']+", name.lower())
             if len(w) > 3 and w not in ("della", "delle", "degli", "dello", "dell", "alla", "nella")]
    if words:
        try:
            res = scryfall_get("/cards/search", q="lang:it " + " ".join(words), unique="cards")
            if res.get("data"):
                return res["data"], "it-loose"
        except urllib.error.HTTPError:
            pass
    return [], None


def slim(c):
    return {
        "name": c["name"],
        "printed_name_it": c.get("printed_name"),
        "scryfall_id": c["id"],
        "oracle_id": c.get("oracle_id"),
        "mana_cost": c.get("mana_cost"),
        "cmc": c.get("cmc"),
        "type_line": c.get("type_line"),
        "color_identity": c.get("color_identity"),
        "oracle_text": c.get("oracle_text"),
    }


def resolve(name):
    c, how = try_named(name)
    if c:
        return slim(c), how, []
    candidates, how = try_italian(name)
    if len(candidates) == 1:
        return slim(candidates[0]), how, []
    if len(candidates) > 1:
        return None, "ambigua", [f"{x['name']} ({x.get('printed_name')})" for x in candidates[:6]]
    return None, "non trovata", []


def main():
    src = sys.stdin if (len(sys.argv) < 2 or sys.argv[1] == "-") else open(sys.argv[1], encoding="utf-8")
    resolved, problems = [], []
    for line in src:
        parsed = parse_line(line)
        if not parsed:
            continue
        qty, name = parsed
        card, how, candidates = resolve(name)
        if card:
            card["quantity"] = qty
            card["input"] = name
            resolved.append(card)
        else:
            problems.append({"input": name, "reason": how, "candidates": candidates})

    total = sum(c["quantity"] for c in resolved)
    print(json.dumps({"resolved": resolved, "total_cards": total, "problems": problems},
                     ensure_ascii=False, indent=1))
    if problems:
        print(f"\nATTENZIONE: {len(problems)} righe da chiarire con l'utente:", file=sys.stderr)
        for p in problems:
            extra = f" — candidate: {', '.join(p['candidates'])}" if p["candidates"] else ""
            print(f"  [{p['reason']}] {p['input']}{extra}", file=sys.stderr)


if __name__ == "__main__":
    main()
