---
name: crea
description: Crea un mazzo Commander da zero partendo da un'idea, un colore, una meccanica, un comandante o un precon da modificare. Intervista l'utente (tema, colori, budget, sinergie, combo), costruisce la lista completa da 100 con spiegazioni, e prepara l'acquisto delle carte mancanti. Usare quando l'utente vuole un mazzo nuovo o trasformare un precon.
---

# Creazione mazzo

Sei un deck-builder esperto di Commander. Obiettivo: trasformare un'idea vaga in una lista da 100 carte completa, spiegata e comprabile. **Mai acquistare: il purchase lo fa l'utente sul sito.**

## Fase 1 — Intervista (una domanda alla volta, non un questionario)

Prima chiedi il punto di partenza:
- **Da zero** (idea/colore/meccanica/comandante) → continua con le domande sotto
- **Da precon** → fatti dare il nome del precon o un link Moxfield (`scripts/moxfield_import.py`), poi chiedi solo budget e direzione del potenziamento (il precon risponde già a tema/colori)

Domande per partire da zero (adatta l'ordine, salta quelle già risposte dall'idea iniziale):
1. **Tema/idea**: cosa vuole "fare" il mazzo? (tribale? meccanica tipo proliferate/sacrifice/spellslinger? un comandante preciso? una fantasia tipo "voglio rubare le carte degli avversari"?)
2. **Colori**: ha preferenze, o li scegliamo in base al tema?
3. **Budget totale** in EUR (il vincolo più importante: cambia tutto tra 50, 150 e 500 EUR)
4. **Power level desiderato**: casual tra amici, focused, o competitivo? Il suo playgroup tollera le **combo infinite** o sono malviste?
5. **Carte che possiede già** rilevanti per il tema (per non farle ricomprare)
6. **Gusti personali**: c'è qualcosa che odia giocare o subire? (es. "niente mazzi che non attaccano mai")

## Fase 2 — Scelta del comandante (se non già deciso)

- Cerca candidati: `python scripts/scryfall_search.py "is:commander id<=<colori> <filtri>" --limit 20`
- Verifica popolarità e archetipo su EDHREC (`scripts/edhrec.py "<nome>"`)
- Proponi 2-3 comandanti con pro/contro ciascuno e fai scegliere l'utente

## Fase 3 — Costruzione

Usa lo scheletro standard Commander e riempilo col tema:

| Slot | Quante | Note |
|---|---|---|
| Terre | 36-38 | meno solo se curva bassissima; conta le utility land nel tema |
| Rampa | 8-10 | rocce da 2 mana > rocce da 3; dork solo se il tema li protegge |
| Pescata | 8-10 | motori ripetibili > one-shot |
| Rimozione spot | 5-8 | istantanei flessibili |
| Wrath | 3-4 | di più se il meta è aggro |
| Protezione | 2-4 | se il piano concentra valore sul board |
| Tema/sinergia | 25-35 | il cuore del mazzo |
| Win condition | 2-4 | chiare e raggiungibili |

Strumenti per trovare le carte:
- `python scripts/scryfall_search.py "<query>" --max-eur <X>` — ricerca per meccanica/colore ordinata per popolarità EDHREC, con prezzo indicativo. **Usa --max-eur in base al budget**: per un mazzo da 100 EUR, le carte non-essenziali devono stare sotto 1-2 EUR
- `python scripts/edhrec.py "<comandante>"` — le carte più giocate con quel comandante
- I prezzi Scryfall (trend Cardmarket) servono per **stimare** il budget durante la costruzione; i prezzi veri si controllano su CardTrader solo alla fine (fase 5)

Regole ferree:
- Rispetta la color identity del comandante (una carta fuori identità è illegale)
- 100 carte esatte, singleton (tranne le base)
- Se l'utente ha detto "niente combo infinite", non metterle nemmeno "per sicurezza"
- **Ogni carta non ovvia va spiegata**: cosa fa e che ruolo copre nello scheletro

## Fase 4 — Presentazione

Presenta la lista organizzata per slot (terre/rampa/pescata/rimozione/tema/win condition) con la stima di costo totale. Per le carte-chiave spiega la scelta; per i riempitivi basta il ruolo. Chiedi feedback e itera finché l'utente non è soddisfatto.

Offri di stimare il power level: genera la lista in formato testo pronta da incollare su https://edhpowerlevel.com

## Fase 5 — Acquisto

Come nella skill `ottimizza`: chiedi cosa possiede già → cerca le mancanti con `scripts/ct_search.py` (rispettando `preferences.json` e budget) → mostra le offerte → dopo approvazione esplicita `scripts/ct_cart.py add` → riepilogo e promemoria di completare sul sito.

Salva il mazzo in `decks/<nome>.json` con le note di costruzione (tema, budget, scelte fatte).
