#!/usr/bin/env python3
"""
Telegram Bot for Team Formation Management
Handles time-restricted submissions and admin oversight
"""

import telebot
import os
from datetime import datetime, time
import logging
import threading
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration  
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# In-memory storage for formations
formazioni = {}

def is_within_time(start_hour, end_hour):
    """
    Check if current time is within the specified hour range
    
    Args:
        start_hour (int): Starting hour (24-hour format)
        end_hour (int): Ending hour (24-hour format)
    
    Returns:
        bool: True if current time is within range
    """
    now = datetime.now().time()
    start_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    
    return start_time <= now <= end_time

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Welcome message for new users"""
    welcome_text = """
🏆 **Bot Formazioni Squadra**

Comandi disponibili:
• `/formazione <tua_formazione>` - Invia la tua formazione (solo in privato, dalle 17:00 alle 19:00)
• `/help` - Mostra questo messaggio di aiuto

**Note:**
- Le formazioni possono essere inviate solo in chat privata con il bot
- Orario consentito: dalle 09:00 alle 19:00
- Le formazioni rimangono segrete fino alla revisione dell'admin
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    """Help command"""
    help_text = """
📋 **Guida Bot Formazioni**

**Per i giocatori:**
• `/formazione <la_tua_formazione>` - Invia la formazione
  - Deve essere inviata in privato al bot
  - Disponibile solo dalle 09:00 alle 19:00
  - Esempio: `/formazione 4-3-3 con Ronaldo titolare`

**Regole:**
• Solo messaggi privati accettati per le formazioni
• Finestra temporale: 09:00 - 19:00
• Ogni utente può inviare/aggiornare la propria formazione
• Le formazioni sono confidenziali

**Stato attuale:**
• Formazioni ricevute: {}
• Orario attuale: {}
• Sottomissioni attive: {}
    """.format(
        len(formazioni),
        datetime.now().strftime("%H:%M"),
        "Sì" if is_within_time(9, 19) else "No"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['formazione'])
def ricevi_formazione(message):
    """
    Handle formation submissions from users
    Only accepts private messages within specified time window
    """
    # Check if message is in private chat
    if message.chat.type != 'private':
        bot.reply_to(message, "🚫 Invia la formazione solo in privato al bot.")
        logger.warning(f"User {message.from_user.username} tried to send formation in non-private chat")
        return
    
    # Check time restriction
    if not is_within_time(9, 19):
        current_time = datetime.now().strftime("%H:%M")
        bot.reply_to(message, f"⏱️ Puoi inviare la formazione solo tra le 09:00 e le 19:00.\nOrario attuale: {current_time}")
        logger.info(f"User {message.from_user.username} tried to send formation outside allowed hours")
        return
    
    # Extract formation text
    formation_text = message.text[len('/formazione'):].strip()
    
    if not formation_text:
        bot.reply_to(message, "❌ Inserisci la tua formazione dopo il comando.\nEsempio: `/formazione 4-3-3 con Messi titolare`")
        return
    
    # Get user identifier
    user_identifier = message.from_user.username or message.from_user.first_name or f"user_{message.from_user.id}"
    
    # Store formation
    formazioni[user_identifier] = {
        'formation': formation_text,
        'timestamp': datetime.now(),
        'user_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'username': message.from_user.username
    }
    
    bot.reply_to(message, "✅ Formazione ricevuta in segreto!\n🔒 La tua formazione è stata registrata e rimarrà confidenziale.")
    logger.info(f"Formation received from {user_identifier}")

@bot.message_handler(commands=['punteggi'])
def mostra_punteggi(message):
    welcome_text = """
🏆 **Punteggi**
Samu: 5
Doc: 5
Andrea: 5
Pesca Medio: 5
Nazza: 4
Pasquale: 4
JJ Pesca: 4
Fabio: 3
Mozza: 3
Aragosta: 3
Simo Gemello: 3
Piccio: 2
Mangio: 2
Zio: 2
Ema: 1
Prio: 1
Ste: 1
Pesca: 1
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['mostraformazioni'])
def mostra_formazioni(message):
    """
    Display all submitted formations (admin only)
    """
    # Check admin privileges
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "❌ Non hai i permessi per usare questo comando.")
        logger.warning(f"Unauthorized access attempt by {message.from_user.username}")
        return
    
    # Check if there are any formations
    if not formazioni:
        bot.reply_to(message, "📭 Nessuna formazione ricevuta finora.")
        return
    
    # Build response with all formations
    response = f"🏆 **Formazioni Ricevute** ({len(formazioni)} totali)\n\n"
    
    for i, (user, data) in enumerate(formazioni.items(), 1):
        timestamp = data['timestamp'].strftime("%H:%M:%S")
        formation = data['formation']
        first_name = data.get('first_name', 'N/A')
        
        response += f"**{i}. {user}** ({first_name})\n"
        response += f"⏰ {timestamp}\n"
        response += f"📋 {formation}\n\n"
    
    # Send response (split if too long)
    if len(response) > 4096:  # Telegram message limit
        # Split into multiple messages
        parts = []
        current_part = f"🏆 **Formazioni Ricevute** ({len(formazioni)} totali)\n\n"
        
        for i, (user, data) in enumerate(formazioni.items(), 1):
            timestamp = data['timestamp'].strftime("%H:%M:%S")
            formation = data['formation']
            first_name = data.get('first_name', 'N/A')
            
            entry = f"**{i}. {user}** ({first_name})\n⏰ {timestamp}\n📋 {formation}\n\n"
            
            if len(current_part + entry) > 4000:
                parts.append(current_part)
                current_part = entry
            else:
                current_part += entry
        
        if current_part:
            parts.append(current_part)
        
        for part in parts:
            bot.send_message(message.chat.id, part)
    else:
        bot.send_message(message.chat.id, response)
    
    logger.info(f"Admin {ADMIN_USERNAME} viewed all formations")

@bot.message_handler(commands=['clearformazioni'])
def clear_formazioni(message):
    """
    Clear all formations (admin only)
    """
    # Check admin privileges
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "❌ Non hai i permessi per usare questo comando.")
        return
    
    formation_count = len(formazioni)
    formazioni.clear()
    
    bot.reply_to(message, f"🗑️ Cancellate {formation_count} formazioni.")
    logger.info(f"Admin {ADMIN_USERNAME} cleared all formations")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    """
    Show bot statistics (admin only)
    """
    # Check admin privileges
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "❌ Non hai i permessi per usare questo comando.")
        return
    
    current_time = datetime.now().strftime("%H:%M:%S")
    submissions_active = "Sì" if is_within_time(9, 19) else "No"
    
    stats_text = f"""
📊 **Statistiche Bot**

• Formazioni totali: {len(formazioni)}
• Orario attuale: {current_time}
• Sottomissioni attive: {submissions_active}
• Admin: {ADMIN_USERNAME}
• Finestra oraria: 09:00 - 19:00

**Utenti attivi:**
{chr(10).join([f"• {user}" for user in formazioni.keys()]) if formazioni else "Nessuno"}
    """
    
    bot.reply_to(message, stats_text)

@bot.message_handler(func=lambda message: True)
def handle_unknown_messages(message):
    """Handle unknown messages and commands"""
    if message.chat.type == 'private':
        bot.reply_to(message, 
                    "❓ Comando non riconosciuto.\n"
                    "Usa `/help` per vedere i comandi disponibili.\n"
                    "Per inviare una formazione usa: `/formazione <tua_formazione>`")
    # Ignore messages in groups to avoid spam

def keep_alive():
    """Keep the bot alive by pinging Telegram API every 5 minutes"""
    def ping():
        while True:
            try:
                # Simple ping to Telegram API to keep connection alive
                bot.get_me()
                logger.info("Keep-alive ping sent")
            except Exception as e:
                logger.warning(f"Keep-alive ping failed: {e}")
            
            # Wait 5 minutes (300 seconds)
            threading.Event().wait(300)
    
    # Start the keep-alive thread
    ping_thread = threading.Thread(target=ping, daemon=True)
    ping_thread.start()
    logger.info("Keep-alive mechanism started (5-minute intervals)")

def main():
    if not TOKEN:
        logger.error('TELEGRAM_TOKEN non impostato. Imposta la variabile d\'ambiente TELEGRAM_TOKEN e riavvia.')
        raise SystemExit(1)

    """Main function to start the bot"""
    logger.info(f"Starting Telegram Bot for Team Formations...")
    logger.info(f"Admin: {ADMIN_USERNAME}")
    logger.info(f"Submission hours: 09:00 - 19:00")
    
    # Start keep-alive mechanism
    keep_alive()
    
    try:
        # Start polling
        bot.infinity_polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
        raise

if __name__ == "__main__":
    main()
