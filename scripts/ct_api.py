# -*- coding: utf-8 -*-
"""Client minimale per CardTrader API v2 e Scryfall. Solo libreria standard.

Il token viene letto da .env (riga CARDTRADER_TOKEN=...) cercato nella
directory corrente e poi risalendo fino alla root del progetto.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

# Su Windows stdout/stderr di default sono cp1252 e vanno in crash su simboli
# come '-' (minus, U+2212) nel testo delle carte (es. abilita' planeswalker).
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

CT_BASE = "https://api.cardtrader.com/api/v2"
SCRYFALL_BASE = "https://api.scryfall.com"
USER_AGENT = "AgenteDeLiMostri/1.0"

_token_cache = None


def find_env(start=None):
    d = os.path.abspath(start or os.getcwd())
    while True:
        p = os.path.join(d, ".env")
        if os.path.isfile(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def get_token():
    global _token_cache
    if _token_cache:
        return _token_cache
    if os.environ.get("CARDTRADER_TOKEN"):
        _token_cache = os.environ["CARDTRADER_TOKEN"]
        return _token_cache
    env = find_env(os.path.dirname(os.path.abspath(__file__))) or find_env()
    if env:
        for line in open(env, encoding="utf-8"):
            line = line.strip()
            if line.startswith("CARDTRADER_TOKEN="):
                _token_cache = line.split("=", 1)[1].strip()
                return _token_cache
    sys.exit("ERRORE: token CardTrader non trovato. Crea un file .env con CARDTRADER_TOKEN=<token> (vedi skill setup).")


def _request(url, payload=None, auth=False, method=None, retries=4):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if auth:
        headers["Authorization"] = f"Bearer {get_token()}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = int(e.headers.get("Retry-After", 0)) or (5 * (attempt + 1))
                print(f"[rate limit] {url} -> attendo {wait}s e riprovo ({attempt+1}/{retries})...",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def ct_get(path, **params):
    url = f"{CT_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return _request(url, auth=True)


def ct_post(path, payload):
    if path.strip("/").endswith("cart/purchase"):
        raise RuntimeError("VIETATO: l'agente non esegue mai l'acquisto. L'utente conferma sul sito.")
    return _request(f"{CT_BASE}{path}", payload=payload, auth=True)


def scryfall_get(path, **params):
    url = f"{SCRYFALL_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    time.sleep(0.15)  # cortesia rate-limit Scryfall (max 10 req/s raccomandato)
    return _request(url)


def scryfall_post(path, payload):
    time.sleep(0.15)
    return _request(f"{SCRYFALL_BASE}{path}", payload=payload)


if __name__ == "__main__":
    info = ct_get("/info")
    print(f"Connessione OK: app '{info.get('name')}' (user_id {info.get('user_id')})")
