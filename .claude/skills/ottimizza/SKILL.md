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

**Non scegliere automaticamente l'offerta piu' economica in assoluto.** A parita' di velocita' di consegna, se l'offerta piu' economica ha una condizione sensibilmente peggiore (es. Played/Poor) e quella con condizione migliore (es. Near Mint) non costa piu' del doppio, proponi quella di qualita' migliore. Il risparmio di pochi centesimi/euro non vale una carta rovinata se l'alternativa buona costa poco di piu'.

**Limite noto sui tempi di consegna:** il sito CardTrader mostra a volte una stima tipo "+3 settimane" per certi venditori CT Zero, ma questa stima **non e' esposta dall'API** (verificato: il JSON del prodotto/venditore non contiene nessun campo con questo dato). L'unico segnale disponibile via API e' il tag "X-Day Ready" nel nome utente (auto-dichiarato dal venditore, quindi non affidabile al 100%, ma e' quello che c'e'). Per questo: **preferisci sempre venditori con tag "X-Day Ready"** quando la priorita' e' la velocita', e se un'offerta selezionata NON ha questo tag, avvisa esplicitamente l'utente che i tempi di consegna reali non sono verificabili da qui e potrebbero essere lunghi.

### 7. Carrello (solo dopo approvazione esplicita sulle offerte specifiche)
`python scripts/ct_cart.py add <product_id>` per ognuna, poi `python scripts/ct_cart.py show` e ricorda all'utente di completare l'acquisto sul sito.

### 8. Salva
Aggiorna `decks/<nome>.json` con la lista finale e le note (tagli, aggiunte, stato acquisti).

## Extra utili
- "Dove sono le mie carte?" → `python scripts/ct_box.py` (box CT Zero) e `python scripts/ct_box.py orders`
- Power level: genera la lista in formato testo (1 riga per carta) pronta da incollare su https://edhpowerlevel.com (non ha API)
- Per liste di riferimento di altri giocatori: https://moxfield.com e https://edhrec.com
