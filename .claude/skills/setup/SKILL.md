---
name: setup
description: Configurazione guidata al primo avvio dell'Agente de li mostri - token CardTrader, preferenze di acquisto, caricamento mazzi, download Comprehensive Rules. Usare quando l'utente e' nuovo, chiede di configurare, o manca .env/preferences.json.
---

# Setup guidato

Guida l'utente passo passo, in modo amichevole, un passo alla volta (non un muro di istruzioni). Parla la sua lingua.

## 1. Token CardTrader

Controlla se esiste `.env` con `CARDTRADER_TOKEN`. Se manca:

1. Spiega: serve un account CardTrader (gratuito) e un token API personale.
2. Guida: vai su **cardtrader.com → accedi → Profilo → Impostazioni → App API** (in fondo alla pagina) → crea una app → copia il token JWT (inizia con `eyJ...`).
3. Fatti incollare il token in chat e scrivilo tu in `.env` come `CARDTRADER_TOKEN=<token>` nella root del progetto.
4. Avvisa: il token permette acquisti sul suo account — resta solo sul suo computer, mai condividerlo ne' committarlo (il `.gitignore` lo esclude gia').
5. Verifica la connessione: `python scripts/ct_api.py` — deve stampare "Connessione OK".

## 2. Preferenze di acquisto

Chiedi (con domande semplici, una per volta) e salva in `preferences.json` nella root:

```json
{
  "languages": ["en", "it"],
  "min_condition": null,
  "priority": "speed",
  "notes": ""
}
```

- `languages`: quali lingue accetta per le carte (codici: en, it, de, fr, es, jp...)
- `min_condition`: condizione minima ("Near Mint", "Slightly Played", "Moderately Played", "Played") o null = qualsiasi
- `priority`: "speed" (venditori CT Zero / 1-Day Ready anche se costano poco di piu') oppure "price" (sempre il piu' economico)
- `notes`: qualsiasi altra preferenza espressa a parole

## 3. Comprehensive Rules (per la skill judge)

Esegui `python scripts/judge_setup.py` per scaricare le regole complete in `rules/`. Se fallisce, non bloccare il setup: la skill judge puo' comunque usare Scryfall, segnala solo che la ricerca per numero di regola sara' limitata.

## 4. Mazzi

Chiedi se vuole caricare subito i suoi mazzi. Per ognuno:
1. Fatti dare la lista (testo libero va bene, anche nomi italiani con refusi, formato "1 nome carta" o solo "nome carta"; chiedi chi e' il comandante)
2. Risolvi con `python scripts/resolve_cards.py` (passa la lista via file temporaneo o stdin)
3. Se ci sono righe ambigue o non trovate, chiedi chiarimenti all'utente mostrando le candidate
4. Verifica: 100 carte esatte (comandante incluso), tutte dentro la color identity del comandante
5. Salva in `decks/<nome-comandante>.json` con: commander, color_identity, lands, spells, notes

## 5. Chiusura

Riassumi cosa e' configurato e suggerisci i prossimi passi: "ottimizza <mazzo>" per l'analisi, "judge" per domande di regole, oppure chiedere direttamente una carta da comprare.
