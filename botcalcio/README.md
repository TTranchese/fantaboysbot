# Telegram Bot per Gestione Formazioni

Un bot Telegram per la gestione delle formazioni di squadra con sottomissioni a tempo limitato e supervisione admin.

## Caratteristiche

- 🔒 **Sottomissioni Private**: Le formazioni possono essere inviate solo tramite messaggi privati
- ⏰ **Restrizioni Temporali**: Le sottomissioni sono accettate solo dalle 17:00 alle 19:00
- 👤 **Controllo Admin**: Solo l'admin può visualizzare tutte le formazioni
- 💾 **Storage in Memoria**: Le formazioni sono memorizzate temporaneamente durante la sessione
- 🛡️ **Gestione Errori**: Feedback chiari per accessi non autorizzati e violazioni temporali

## Configurazione

### Variabili d'Ambiente

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export ADMIN_USERNAME="your_admin_username"
