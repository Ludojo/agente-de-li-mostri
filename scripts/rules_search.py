# -*- coding: utf-8 -*-
"""Cerca nelle Comprehensive Rules locali (scaricate con judge_setup.py).

Uso:
  python scripts/rules_search.py 702.19            (regola per numero, con sottoregole)
  python scripts/rules_search.py "deathtouch"      (ricerca parola chiave)
  python scripts/rules_search.py "menace" --max 20
"""
import os
import re
import sys

RULE_NUM_RE = re.compile(r"^\d{3}(\.\d+[a-z]?)?$")


def load_rules():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "rules", "comprehensive_rules.txt")
    if not os.path.isfile(path):
        sys.exit("Comprehensive Rules non trovate. Esegui prima: python scripts/judge_setup.py")
    raw = open(path, encoding="utf-8", errors="ignore").read()
    return raw.splitlines()


def by_number(lines, num):
    prefix = num if num.endswith(".") else num
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith(prefix):
            out.append(s)
        elif out and re.match(r"^\d{3}\.", s) and not s.startswith(prefix):
            # nuova regola: se avevamo gia' preso il blocco e questa non matcha, stop
            if not s.startswith(num.split(".")[0] + "."):
                break
    return out


def by_keyword(lines, kw, max_hits):
    kw_l = kw.lower()
    out = []
    for line in lines:
        s = line.strip()
        if kw_l in s.lower() and re.match(r"^\d{3}\.", s):
            out.append(s)
            if len(out) >= max_hits:
                break
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    query = sys.argv[1]
    max_hits = 12
    if "--max" in sys.argv:
        max_hits = int(sys.argv[sys.argv.index("--max") + 1])

    lines = load_rules()
    if RULE_NUM_RE.match(query):
        hits = by_number(lines, query)
        if not hits:
            hits = by_keyword(lines, query, max_hits)
    else:
        hits = by_keyword(lines, query, max_hits)

    if not hits:
        print(f"Nessuna regola trovata per: {query}")
        return
    for h in hits:
        print(h)


if __name__ == "__main__":
    main()
