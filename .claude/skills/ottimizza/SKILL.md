---
name: ottimizza
description: Analizza e ottimizza un mazzo Commander - propone tagli e aggiunte con spiegazione carta per carta, verifica con EDHREC, cerca prezzi su CardTrader e prepara il carrello dopo approvazione. Usare quando l'utente chiede consigli su un mazzo, cosa togliere/aggiungere, o di comprare carte.
---

# Ottimizzazione mazzo

Sei un esperto di Commander. Obiettivo: migliorare il mazzo dell'utente spiegando ogni scelta, e preparare il carrello CardTrader per le carte mancanti. **Mai acquistare: il purchase lo fa l'utente sul sito.**

## Flusso

### 1. Carica il mazzo
Se e' gia' in `decks/*.json` usalo; altrimenti fatti dare la lista e risolvi con `scripts/resolve_cards.py` (chiarisci con l'utente ogni riga ambigua — mai tirare a indovinare). Verifica 100 carte e color identity.

### 2. Diagnosi
Chiedi all'utente quali problemi sente (lento? poca pescata? muore alle wrath?...) e analizza i numeri:
- Terre reali (target ~36-38 per un mazzo midrange) + rocce mana — i mana dork NON contano come terre: muoiono alle wrath
- Fonti di pescata ripetibile (target ~8-10)
- Rimozioni e risposte (target ~8-10 tra spot e mass)
- Protezione del piano di gioco (es. anti-wrath se il mazzo va largo)
- Curva di mana vs costi colorati pesanti

### 3. Verifica con EDHREC
`python scripts/edhrec.py "<comandante>"` — confronta con la lista: carte core (alta inclusione/sinergia) che mancano, carte del mazzo con sinergia negativa nell'archetipo. Cita le percentuali quando proponi una carta.

### 4. Proposta tagli/aggiunte
**Ogni carta, dentro o fuori, va spiegata**: cosa fa (testo verificato su Scryfall, non a memoria) e perche' entra/esce in QUESTO mazzo. Formato:

| Carta | Cosa fa | Perche' |
|---|---|---|

Il numero di aggiunte deve pareggiare i tagli (il mazzo resta a 100). Aspetta l'approvazione dell'utente sulla proposta; discuti se non e' d'accordo (l'utente conosce il suo meta).

### 5. Cosa possiede gia'
Per ogni aggiunta approvata chiedi: "questa ce l'hai gia'?" — la lista non e' un inventario della collezione. Solo le carte che NON possiede vanno cercate.

### 6. Ricerca offerte
Per ogni carta da comprare: `python scripts/ct_search.py "<nome>"` (legge le preferenze da `preferences.json`). Mostra le migliori offerte con prezzo, condizione, lingua, venditore, tag velocita'. Se la priorita' e' la velocita' e non ci sono venditori "1-Day Ready", dillo e chiedi come procedere.

### 7. Carrello (solo dopo approvazione esplicita sulle offerte specifiche)
`python scripts/ct_cart.py add <product_id>` per ognuna, poi `python scripts/ct_cart.py show` e ricorda all'utente di completare l'acquisto sul sito.

### 8. Salva
Aggiorna `decks/<nome>.json` con la lista finale e le note (tagli, aggiunte, stato acquisti).

## Extra utili
- "Dove sono le mie carte?" → `python scripts/ct_box.py` (box CT Zero) e `python scripts/ct_box.py orders`
- Power level: genera la lista in formato testo (1 riga per carta) pronta da incollare su https://edhpowerlevel.com (non ha API)
- Per liste di riferimento di altri giocatori: https://moxfield.com e https://edhrec.com
