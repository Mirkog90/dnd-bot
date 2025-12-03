# 🎲 D&D Telegram Bot - Guida Completa di Setup

## 📋 Contenuto Progetto

Questo progetto include:
- `dnd_bot.py` - Script principale del bot
- `dnd_database.json` - Database D&D 5e/5.2024 con lore
- Istruzioni di setup e deployment

---

## 🔧 STEP 1: Installazione Locale (Windows/Mac/Linux)

### Prerequisiti
- Python 3.8+ installato ([download qui](https://www.python.org/downloads/))
- Pip (viene con Python)

### Installazione delle Dipendenze

Apri il terminale/cmd nella cartella del progetto e esegui:

```bash
pip install python-telegram-bot requests schedule
```

**Pacchetti installati:**
- `python-telegram-bot` - Libreria ufficiale Telegram
- `requests` - Per API HTTP
- `schedule` - Per scheduling automatico

---

## 🚀 STEP 2: Configurazione del Bot

### Il tuo Token è già configurato nello script:
```
TOKEN = "8261893583:AAHFLCvG88RG3jcG4U-GCLUMF3P8yumxhGE"
CHAT_ID = 20102132
```

**⚠️ IMPORTANTE**: Non condividere mai il token con nessuno!

---

## 🎯 STEP 3: Avvio del Bot

### Test Locale (Primo Avvio)

Dalla cartella del progetto:

```bash
python dnd_bot.py
```

Se tutto funziona, vedrai nel terminale:
```
Bot avviato! In ascolto per messaggi...
Orari pianificati: 13:00 e 21:00 CET
```

### Test Manuale

Invia un messaggio al bot su Telegram e vedrai una risposta di conferma.

---

## ☁️ STEP 4: Hosting 24/7 Gratuito (CONSIGLIATO)

Per avere il bot sempre acceso senza tenere il PC acceso, usa **Replit** (gratuito, semplice):

### Setup Replit

1. **Vai su** [replit.com](https://replit.com) e registrati
2. **Click "Create"** → **"Import from GitHub"**
3. Copia il link di questo progetto (o carica i file manualmente)
4. **Seleziona "Python"** come linguaggio
5. **Click "Import"**
6. **Replit installerà automaticamente** le dipendenze

### Eseguire su Replit

1. Click il bottone **"Run"** (in alto)
2. Il bot partirà e rimarrà acceso 24/7
3. Riceverai i messaggi automaticamente alle 13:00 e 21:00 CET

### Mantenere il Bot Acceso (Uptime Forever)

Replit chiude lo script dopo 1 ora di inattività. Per rimanere sempre acceso:

**Opzione A: Usa UptimeRobot (Gratuito)**
1. Vai su [uptimerobot.com](https://uptimerobot.com)
2. Registrati gratuitamente
3. Crea un "Monitor" HTTP che fa ping al tuo Replit ogni 5 minuti
4. Il bot rimarrà sveglio indefinitamente

**Opzione B: Upgrade Replit a Pagamento**
- Replit Plus ($7/mese) = Bot sempre acceso
- (Consigliato se usi spesso Replit)

---

## 📊 Struttura del Database

Il file `dnd_database.json` contiene:

```json
{
  "lore_entries": [
    {
      "id": 1,
      "title": "Nome dell'argomento",
      "category": "Razze | Divinità | Mostri | Piani | Artefatti | Storia",
      "content": "Testo di 10+ righe",
      "image_url": "URL immagine (opzionale)",
      "related_id": null (o ID collegato),
      "spoiler_campaign": false,
      "date_added": "2025-12-03"
    }
  ]
}
```

---

## 🔄 Come Funziona il Bot

### Logica Scheduling

- **Ogni giorno** alle **13:00 CET** → Manda 1° messaggio
- **Ogni giorno** alle **21:00 CET** → Manda 2° messaggio
- **Messaggi collegati**: Se esiste un `related_id`, il 2° messaggio approfondisce il tema del 1°
- **Nessuna ripetizione**: Il bot tiene traccia di cosa ha già mandato
- **Database ordinato**: Gli argomenti sono randomizzati ma progressivi

---

## 📝 Aggiungere Nuovi Contenuti

### Aggiungere una Voce al Database

Apri `dnd_database.json` e aggiungi un nuovo elemento:

```json
{
  "id": [numero_progressivo],
  "title": "Il Nome del Tuo Argomento",
  "category": "Razze",
  "content": "Scrivi il tuo contenuto qui. Ricordati di fare 10+ righe...",
  "image_url": "https://example.com/immagine.jpg",
  "related_id": null,
  "spoiler_campaign": false,
  "date_added": "2025-12-03"
}
```

**Note:**
- `image_url` può essere null se non hai un'immagine
- `related_id` collega 2 messaggi (es: 1° messaggio su Drow, 2° messaggio su Underdark)
- `spoiler_campaign` = true per argomenti delle campagne ufficiali (salterà questi)

---

## 🛑 Fermare il Bot

### Su Computer Locale
- Premi **Ctrl + C** nel terminale

### Su Replit
- Click il bottone **"Stop"**

### Per Sempre
- Cancella `bot_state.json` (resetta la lista di messaggi inviati)

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'telegram'"
→ Esegui: `pip install python-telegram-bot`

### "Bot non invia messaggi"
→ Verifica che il token sia corretto nel codice

### "Il bot va offline su Replit"
→ Usa UptimeRobot per mantenerlo acceso (vedi Step 4, Opzione A)

### "I messaggi si ripetono"
→ Cancella `bot_state.json` per resettare la cronologia

---

## 📧 File Generat Automaticamente

Quando il bot parte, crea:

- **`bot_state.json`** - Cronologia messaggi inviati (NO TOCCARE)
- **`bot_log.txt`** - Log delle operazioni

---

## 🎯 Prossimi Passi

1. ✅ Installa Python e le dipendenze
2. ✅ Configura il token (già fatto)
3. ✅ Avvia il bot localmente per testare
4. ✅ Carica su Replit per avere acceso 24/7
5. ✅ (Opzionale) Configura UptimeRobot per uptime garantito

**Buon divertimento con la lore di D&D!** 🎲✨
