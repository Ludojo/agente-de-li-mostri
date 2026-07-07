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

from ct_api import scryfall_get, scryfall_post

QTY_RE = re.compile(r"^\s*(\d+)\s*[xX]?\s+(.\S*.*)$")

# Terre base italiane: risolte a colpo sicuro, MAI via fuzzy match inglese.
# ("Isola" fuzzy-matchava "Isolate" (carta bianca sbagliata) prima di questo fix.)
BASIC_LANDS_IT = {
    "pianura": "Plains", "pianure": "Plains",
    "isola": "Island", "isole": "Island",
    "palude": "Swamp", "paludi": "Swamp",
    "foresta": "Forest", "foreste": "Forest",
    "montagna": "Mountain", "montagne": "Mountain",
    "landa desolata": "Wastes", "lande desolate": "Wastes",
}


def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    m = QTY_RE.match(line)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return 1, line


def try_exact(name):
    try:
        return scryfall_get("/cards/named", exact=name), "exact"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise
        return None, None


def try_fuzzy(name):
    try:
        return scryfall_get("/cards/named", fuzzy=name), "fuzzy"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise
        return None, None


def try_italian_exact(name):
    """Nome stampato italiano, frase esatta tra virgolette: preciso, va tentato presto."""
    try:
        res = scryfall_get("/cards/search", q=f'lang:it "{name}"', unique="cards")
        return res.get("data", []), "it-exact"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise
        return [], None


def try_italian_loose(name):
    """Nome stampato italiano per parole chiave: approssimato, solo come ultima spiaggia."""
    words = [w for w in re.findall(r"[a-zà-ù']+", name.lower())
             if len(w) > 3 and w not in ("della", "delle", "degli", "dello", "dell", "alla", "nella")]
    if not words:
        return [], None
    try:
        res = scryfall_get("/cards/search", q="lang:it " + " ".join(words), unique="cards")
        return res.get("data", []), "it-loose"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise
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
    basic = BASIC_LANDS_IT.get(name.strip().lower())
    if basic:
        c, _ = try_exact(basic)
        if c:
            return slim(c), "terra base", []

    # 1) match esatti (deterministici, zero rischio di scambiare carta)
    c, how = try_exact(name)
    if c:
        return slim(c), how, []
    it_exact, it_exact_how = try_italian_exact(name)
    if len(it_exact) == 1:
        return slim(it_exact[0]), it_exact_how, []
    if len(it_exact) > 1:
        return None, "ambigua", [f"{x['name']} ({x.get('printed_name')})" for x in it_exact[:6]]

    # 2) match approssimati (rischio di falsi positivi, es. "Isola" ~ "Isolate": usati solo come ultima spiaggia)
    c, how = try_fuzzy(name)
    if c:
        return slim(c), how, []
    it_loose, it_loose_how = try_italian_loose(name)
    if len(it_loose) == 1:
        return slim(it_loose[0]), it_loose_how, []
    if len(it_loose) > 1:
        return None, "ambigua", [f"{x['name']} ({x.get('printed_name')})" for x in it_loose[:6]]

    return None, "non trovata", []


def batch_exact(entries):
    """Prova a risolvere tutte le righe in blocco con /cards/collection (75 per richiesta,
    match esatto EN case-insensitive). Riduce di ~50x le richieste per liste in inglese.
    Ritorna (risolte: dict input->card, rimanenti: list entries)."""
    todo = [(qty, name) for qty, name in entries
            if name.strip().lower() not in BASIC_LANDS_IT]
    hits = {}
    names = list(dict.fromkeys(name for _, name in todo))
    for i in range(0, len(names), 75):
        chunk = names[i:i + 75]
        try:
            res = scryfall_post("/cards/collection", {"identifiers": [{"name": n} for n in chunk]})
        except urllib.error.HTTPError:
            return {}, entries  # fallback totale al percorso riga-per-riga
        found_names = {}
        for c in res.get("data", []):
            found_names[c["name"].lower()] = c
        for n in chunk:
            c = found_names.get(n.lower())
            if c:
                hits[n] = slim(c)
    remaining = [(qty, name) for qty, name in entries if name not in hits]
    return hits, remaining


def main():
    src = sys.stdin if (len(sys.argv) < 2 or sys.argv[1] == "-") else open(sys.argv[1], encoding="utf-8")
    entries = []
    for line in src:
        parsed = parse_line(line)
        if parsed:
            entries.append(parsed)

    resolved, problems = [], []
    rate_limited_at = None

    batch_hits, remaining = batch_exact(entries)
    for qty, name in entries:
        if name in batch_hits:
            card = dict(batch_hits[name])
            card["quantity"] = qty
            card["input"] = name
            resolved.append(card)

    for qty, name in remaining:
        try:
            card, how, candidates = resolve(name)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                rate_limited_at = name
                break
            raise
        if card:
            card["quantity"] = qty
            card["input"] = name
            resolved.append(card)
        else:
            problems.append({"input": name, "reason": how, "candidates": candidates})

    total = sum(c["quantity"] for c in resolved)
    if rate_limited_at:
        print(f"\nERRORE: Scryfall ha rate-limitato la sessione (troppe richieste in poco tempo). "
              f"Interrotto a '{rate_limited_at}'. Le {len(resolved)} carte gia' risolte sono salve qui sotto; "
              f"aspetta un minuto e rilancia solo sulle righe rimanenti.", file=sys.stderr)
    print(json.dumps({"resolved": resolved, "total_cards": total, "problems": problems},
                     ensure_ascii=False, indent=1))
    if problems:
        print(f"\nATTENZIONE: {len(problems)} righe da chiarire con l'utente:", file=sys.stderr)
        for p in problems:
            extra = f" — candidate: {', '.join(p['candidates'])}" if p["candidates"] else ""
            print(f"  [{p['reason']}] {p['input']}{extra}", file=sys.stderr)


if __name__ == "__main__":
    main()
