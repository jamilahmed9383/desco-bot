# ⚡ Web and Bot Basse Website

## Features
- Web UI to check DESCO balance.
- Telegram Bot command `/check` or `/check <account_no>`.
- Deployable on Render, PythonAnywhere, etc.

## Deploy on Render
1. Upload this project to GitHub or zip.
2. Connect repo in [Render.com](https://render.com).
3. Add `.env` variables.
4. Start Command: `python app.py`

Webhook URL:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<your-render-url>/<YOUR_BOT_TOKEN>
