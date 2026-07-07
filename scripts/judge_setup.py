# -*- coding: utf-8 -*-
"""Scarica l'ultima versione delle Comprehensive Rules in rules/comprehensive_rules.txt.

Uso: python scripts/judge_setup.py
"""
import os
import re
import urllib.parse
import urllib.request

USER_AGENT = "AgenteDeLiMostri/1.0"
RULES_PAGE = "https://magic.wizards.com/en/rules"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rules_dir = os.path.join(root, "rules")
    os.makedirs(rules_dir, exist_ok=True)

    html = fetch(RULES_PAGE).decode("utf-8", errors="ignore")
    m = re.search(r'https://media\.wizards\.com/[^"\']+MagicCompRules[^"\']*\.txt', html)
    if not m:
        raise SystemExit("Link alle Comprehensive Rules non trovato sulla pagina Wizards. "
                         "Scarica manualmente da https://magic.wizards.com/en/rules in rules/comprehensive_rules.txt")
    url = urllib.parse.quote(m.group(0), safe=":/")
    print(f"Scarico: {url}")
    data = fetch(url)
    out = os.path.join(rules_dir, "comprehensive_rules.txt")
    with open(out, "wb") as f:
        f.write(data)
    print(f"Salvate in {out} ({len(data)//1024} KB)")


if __name__ == "__main__":
    main()
