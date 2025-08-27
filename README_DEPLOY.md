# Bot Calcio (Telegram)

## Avvio locale
1. Python 3.11+
2. `pip install -r requirements.txt`
3. Esporta le variabili d'ambiente:
   - Linux/macOS: `export TELEGRAM_TOKEN=... && export ADMIN_USERNAME=...`
   - Windows (PowerShell): `$env:TELEGRAM_TOKEN="..." ; $env:ADMIN_USERNAME="..."`
4. `python -m botcalcio.main`

## Docker
```
docker build -t botcalcio .
docker run -e TELEGRAM_TOKEN=... -e ADMIN_USERNAME=... --name bot botcalcio
```

## Railway (free ma non sempre 24/7)
1. Collega il repo a Railway
2. Tipo servizio: **Worker**
3. Start Command: `python -m botcalcio.main`
4. Variabili: `TELEGRAM_TOKEN`, `ADMIN_USERNAME`

## VPS (sempre on, gratuito con Oracle Free Tier)
Crea un servizio systemd con `botcalcio.service`:

```
# /etc/systemd/system/botcalcio.service
[Unit]
Description=Bot Calcio Telegram
After=network.target

[Service]
WorkingDirectory=/opt/botcalcio
Environment=TELEGRAM_TOKEN=...
Environment=ADMIN_USERNAME=...
ExecStart=/usr/bin/python3 -m botcalcio.main
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Comandi:
```
sudo systemctl daemon-reload
sudo systemctl enable --now botcalcio
sudo journalctl -u botcalcio -f
```
