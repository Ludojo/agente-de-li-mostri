# 🐉 Agente de li mostri

Assistente AI per Magic: The Gathering (formato Commander/EDH). Ottimizza i tuoi mazzi con spiegazioni carta per carta, trova i prezzi migliori su CardTrader e prepara il carrello per te. Include una skill **Judge** per risolvere dubbi di regole e controversie al tavolo.

> ⚠️ **L'agente non compra mai nulla da solo.** Prepara il carrello su CardTrader; l'acquisto finale lo confermi sempre tu sul sito.

## Cosa fa

- **Setup guidato**: al primo avvio ti aiuta a configurare il token CardTrader e a caricare i tuoi mazzi
- **Ottimizzazione mazzi**: analizza la lista (anche scritta in italiano, con refusi), la incrocia con [EDHREC](https://edhrec.com) e ti propone tagli e aggiunte — **ogni carta con la spiegazione di cosa fa e perché entra o esce**
- **Acquisti intelligenti**: cerca le offerte migliori su CardTrader rispettando le tue preferenze (lingua, condizione, velocità di consegna / CardTrader Zero), e aggiunge al carrello solo dopo la tua approvazione
- **Tracking**: ti dice dove sono le tue carte (box CardTrader Zero, ordini, tempi stimati)
- **Judge**: risponde a domande di regole con testo ufficiale delle carte, ruling ufficiali e Comprehensive Rules, citando le fonti

## Requisiti

- [Claude Code](https://claude.com/claude-code) **oppure** OpenAI Codex (o un altro agente AI che legge `AGENTS.md`)
- Python 3.10+ (gli script usano solo la libreria standard, zero dipendenze)
- Un account [CardTrader](https://www.cardtrader.com) con token API (gratuito, l'agente ti guida a crearlo)

## Installazione

```bash
git clone https://github.com/Ludojo/agente-de-li-mostri.git
cd agente-de-li-mostri
```

**Con Claude Code:** apri la cartella e scrivi `setup` (o semplicemente saluta: l'agente capisce che è il primo avvio e ti guida).

**Con Codex:** apri la cartella; le istruzioni sono in `AGENTS.md`, chiedi di fare il setup.

Il setup ti guida a:
1. Creare il token API su CardTrader (Profilo → Impostazioni → App API) e salvarlo nel file `.env` locale
2. Verificare la connessione
3. Scaricare le Comprehensive Rules per la skill Judge
4. Caricare i tuoi mazzi e le tue preferenze di acquisto

## Sicurezza

- Il token resta **solo sul tuo computer** nel file `.env` (escluso da git tramite `.gitignore`)
- Il token permette acquisti sul tuo account: non condividerlo e non committarlo mai
- L'agente ha il **divieto esplicito di chiamare l'endpoint di acquisto** — prepara il carrello e si ferma lì

## Skill disponibili

| Skill | Cosa fa |
|---|---|
| `setup` | Configurazione guidata primo avvio |
| `ottimizza` | Analisi e ottimizzazione di un mazzo con proposta tagli/aggiunte spiegati |
| `judge` | Domande di regole, ruling ufficiali, controversie da gioco |

## Fonti usate dall'agente

- [Scryfall](https://scryfall.com) — database carte e ruling ufficiali
- [EDHREC](https://edhrec.com) — statistiche di inclusione e sinergia per comandante
- [Moxfield](https://moxfield.com) — liste di riferimento
- [EDHPowerLevel](https://edhpowerlevel.com) — valutazione power level (manuale: l'agente ti prepara la lista da incollare)
- [CardTrader API v2](https://www.cardtrader.com/docs/api/full/reference) — prezzi e acquisti
- Comprehensive Rules, IPG, MTR ([Wizards](https://magic.wizards.com/en/rules), [Italian Magic Judges](https://italianmagicjudges.net/risorse))

## Disclaimer

La skill Judge è uno strumento di supporto, non un giudice certificato: per tornei sanzionati fa fede il giudice in sala. Questo progetto non è affiliato a Wizards of the Coast né a CardTrader.
