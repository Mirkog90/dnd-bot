#!/usr/bin/env python3
"""
🎲 D&D Telegram Bot - Bot di Lore D&D 5e con Scheduling Automatico
Manda messaggi di lore D&D alle 13:00 e 21:00 CET, ogni giorno
Attinge da un database unico senza ripetizioni
"""

import json
import os
import time
import logging
import random
from datetime import datetime
from pathlib import Path
import schedule
from telegram import Bot
from telegram.error import TelegramError
import asyncio

# ==================== CONFIGURAZIONE ====================

TOKEN = "8261893583:AAHFLCvG88RG3jcG4U-GCLUMF3P8yumxhGE"
CHAT_ID = 20102132
DATABASE_FILE = "dnd_database.json"
STATE_FILE = "bot_state.json"
LOG_FILE = "bot_log.txt"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== GESTIONE STATO ====================

def load_state():
    """Carica lo stato del bot (messaggi già inviati)"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"sent_ids": [], "last_sent": {}}
    return {"sent_ids": [], "last_sent": {}}

def save_state(state):
    """Salva lo stato del bot"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def load_database():
    """Carica il database D&D"""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Errore caricamento database: {e}")
            return {"lore_entries": []}
    return {"lore_entries": []}

# ==================== LOGICA MESSAGGI ====================

def get_next_message(database, state, skip_id=None):
    """
    Ottiene il prossimo messaggio disponibile
    - Evita ripetizioni
    - Sceglie in modo casuale
    - Esclude gli ID già inviati
    """
    entries = database.get("lore_entries", [])
    
    # Filtra: esclude messaggi già inviati e spoiler campagne
    available = [
        e for e in entries 
        if e.get("id") not in state["sent_ids"] 
        and not e.get("spoiler_campaign", False)
        and e.get("id") != skip_id
    ]
    
    if not available:
        # Reset: tutti i messaggi sono stati inviati
        logger.info("📊 Database esaurito! Reset della cronologia.")
        state["sent_ids"] = []
        available = [e for e in entries if not e.get("spoiler_campaign", False)]
    
    if not available:
        logger.warning("⚠️ Nessun messaggio disponibile nel database!")
        return None
    
    # Sceglie randomicamente
    message = random.choice(available)
    return message

def format_message(entry, is_connected=False):
    """Formatta un messaggio di lore per Telegram"""
    title = entry.get("title", "Senza Titolo")
    category = entry.get("category", "Lore")
    content = entry.get("content", "")
    
    if is_connected:
        header = f"🔗 **Approfondimento:** {title}\n"
    else:
        header = f"🎲 **{category}:** {title}\n"
    
    message = f"{header}━━━━━━━━━━━━━━━━━━━━━━━━\n\n{content}\n\n━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return message

async def send_message(bot, message_text, image_url=None):
    """Invia un messaggio a Telegram"""
    try:
        if image_url and image_url.strip():
            # Invia con immagine
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=image_url,
                caption=message_text,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Messaggio con immagine inviato alle {datetime.now().strftime('%H:%M:%S')}")
        else:
            # Invia solo testo
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message_text,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Messaggio testuale inviato alle {datetime.now().strftime('%H:%M:%S')}")
        return True
    except TelegramError as e:
        logger.error(f"❌ Errore Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Errore generico: {e}")
        return False

# ==================== TASK SCHEDULING ====================

async def send_daily_message():
    """Task: Invia il messaggio giornaliero (collegato se possibile)"""
    logger.info(f"\n{'='*60}")
    logger.info(f"⏰ TASK SCHEDULING: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*60}")
    
    database = load_database()
    state = load_state()
    bot = Bot(token=TOKEN)
    
    # Ottiene primo messaggio
    message = get_next_message(database, state)
    if not message:
        logger.warning("⚠️ Nessun messaggio da inviare!")
        return
    
    # Formatta e invia
    formatted = format_message(message, is_connected=False)
    success = await send_message(bot, formatted, message.get("image_url"))
    
    if success:
        # Registra come inviato
        state["sent_ids"].append(message["id"])
        state["last_sent"]["first"] = message["id"]
        save_state(state)
        logger.info(f"📝 Registrato: {message['title']} (ID: {message['id']})")
        
        # Controlla se esiste messaggio collegato
        related_id = message.get("related_id")
        if related_id:
            await asyncio.sleep(2)  # Piccola pausa tra messaggi
            
            # Ottiene messaggio collegato
            related = next(
                (e for e in database["lore_entries"] if e["id"] == related_id),
                None
            )
            
            if related:
                formatted_related = format_message(related, is_connected=True)
                success_related = await send_message(bot, formatted_related, related.get("image_url"))
                
                if success_related:
                    state["sent_ids"].append(related["id"])
                    state["last_sent"]["related"] = related["id"]
                    save_state(state)
                    logger.info(f"🔗 Messaggio collegato inviato: {related['title']} (ID: {related['id']})")

# ==================== SCHEDULING ====================

def schedule_tasks():
    """Configura gli orari di scheduling"""
    schedule.every().day.at("13:00").do(lambda: asyncio.run(send_daily_message()))
    schedule.every().day.at("21:00").do(lambda: asyncio.run(send_daily_message()))
    
    logger.info("✅ Bot avviato!")
    logger.info("📅 Orari pianificati: 13:00 e 21:00 CET")
    logger.info("🎲 Database caricato")
    logger.info("⏳ In attesa del prossimo messaggio...")

def run_scheduler():
    """Loop principale dello scheduler"""
    schedule_tasks()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Controlla ogni minuto

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    logger.info("🎲 " + "="*50)
    logger.info("🎲 D&D TELEGRAM BOT - AVVIO")
    logger.info("🎲 " + "="*50)
    logger.info(f"⏰ Ora attuale: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CET')}")
    
    # Verifica file necessari
    if not os.path.exists(DATABASE_FILE):
        logger.error(f"❌ File {DATABASE_FILE} non trovato! Carica il database.")
        exit(1)
    
    logger.info(f"✅ Token configurato: {TOKEN[:20]}...")
    logger.info(f"✅ Chat ID: {CHAT_ID}")
    
    # Avvia scheduler
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot fermato dall'utente")
    except Exception as e:
        logger.error(f"❌ Errore critico: {e}")
