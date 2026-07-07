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

Prima di clonare il repo, assicurati di avere **uno** di questi strumenti AI da terminale già funzionante sul tuo computer. Senza uno di questi non puoi far girare l'agente.

| Strumento | Cosa serve per usarlo | Costo |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) (consigliato) | Account Anthropic con piano **Claude Pro o Max** | A pagamento (abbonamento mensile) |
| [OpenAI Codex](https://openai.com/codex/) | Account OpenAI con **ChatGPT Plus o Pro** | A pagamento (abbonamento mensile) |
| [Google Antigravity](https://antigravity.google/) | Account Google con piano **Gemini** a pagamento | A pagamento (abbonamento mensile) |

**Non vuoi/puoi pagare un abbonamento?** Usa **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** di Google: è gratuito e open source, con una fascia gratuita dell'API sufficiente per un uso non intensivo come questo.
> ⚠️ Non ancora testato su questo repo in modo specifico — le istruzioni sono scritte in `AGENTS.md` (lo standard che Codex legge nativamente) e dovrebbero funzionare anche con Gemini CLI, ma se incontri problemi apri una issue.

In alternativa, tutti e tre gli strumenti a pagamento offrono anche **crediti API a consumo** (paghi solo quello che usi, niente abbonamento fisso) — per un uso occasionale, tipo ottimizzare un mazzo ogni tanto, può costare pochi euro invece di un abbonamento pieno.

Oltre allo strumento AI, ti serve:
- **Python 3.10+** installato sul computer (gli script usano solo la libreria standard, zero dipendenze da installare — verifica con `python --version` o `python3 --version` nel terminale)
- **Git** installato (per clonare il repo — verifica con `git --version`)
- Un account [CardTrader](https://www.cardtrader.com) (gratuito, te lo fai al volo se non ce l'hai — il token API te lo fa creare l'agente stesso durante il setup)

## Installazione

```bash
git clone https://github.com/Ludojo/agente-de-li-mostri.git
cd agente-de-li-mostri
```

Poi apri la cartella con lo strumento che hai scelto e digli semplicemente **"ciao"** — capisce da solo che è il primo avvio e ti guida lui passo passo nel setup. Non serve altro comando speciale, con nessuno dei quattro strumenti.

- **Claude Code**: `claude` nel terminale dentro la cartella del repo
- **Codex**: apri la cartella, le istruzioni sono già in `AGENTS.md`
- **Antigravity / Gemini CLI**: apri la cartella, stesso principio — legge `AGENTS.md`

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
| `crea` | Crea un mazzo nuovo da un'idea/colore/meccanica o trasforma un precon: intervista guidata (tema, budget, combo sì/no), lista completa da 100 spiegata |
| `judge` | Domande di regole, ruling ufficiali, controversie da gioco |

## Fonti usate dall'agente

- [Scryfall](https://scryfall.com) — database carte e ruling ufficiali
- [EDHREC](https://edhrec.com) — statistiche di inclusione e sinergia per comandante
- [Moxfield](https://moxfield.com) — liste di riferimento
- [EDHPowerLevel](https://edhpowerlevel.com) — valutazione power level (manuale: l'agente ti prepara la lista da incollare)
- [CardTrader API v2](https://www.cardtrader.com/docs/api/full/reference) — prezzi e acquisti
- Comprehensive Rules, IPG, MTR ([Wizards](https://magic.wizards.com/en/rules), [Italian Magic Judges](https://italianmagicjudges.net/risorse))

## Problemi comuni

- **"python non è riconosciuto come comando"** → non hai Python installato, o non è nel PATH. Scaricalo da [python.org](https://python.org) (su Windows spunta "Add python.exe to PATH" durante l'installazione) e riapri il terminale.
- **"git non è riconosciuto come comando"** → installa Git da [git-scm.com](https://git-scm.com) e riapri il terminale.
- **Non ho nessuno dei quattro strumenti** → vedi la sezione [Requisiti](#requisiti): scegli Gemini CLI se non vuoi pagare, o valuta i crediti API a consumo prima di prendere un abbonamento pieno.
- **L'agente dice che manca il token CardTrader** → normale al primo avvio, fatti guidare nel setup (basta scrivere "ciao" o "setup").
- **Non so se ho già fatto il setup** → chiedi direttamente all'agente "ho già fatto il setup?", controlla da solo se esistono `.env` e `preferences.json`.

## Disclaimer

La skill Judge è uno strumento di supporto, non un giudice certificato: per tornei sanzionati fa fede il giudice in sala. Questo progetto non è affiliato a Wizards of the Coast né a CardTrader.
