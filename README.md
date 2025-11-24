# Pentest Bot (Ethical IP Logging via Telegram)

This repository contains a full end-to-end ethical penetration-testing system that uses a Telegram bot
to request explicit consent from a tester and then logs (with consent) their IP, headers and approximate geolocation.

**IMPORTANT:** This system must only be used with explicit, written authorization. Do not use this against uninformed users.

## Contents
- bot/: Telegram bot service (aiogram)
- web/: FastAPI backend (test endpoint, session audit, admin export)
- nginx/: nginx config to forward headers and proxy to web
- docker-compose.yml: Compose stack (db, web, bot, nginx)
- .env.example: Environment variables example
- models.sql: Database schema
- export_session.py: Quick CSV export helper
- consent_template.txt: Consent text to include in audit logs
- report_template.md: Pentest report skeleton

## Quick start (local, demonstration only)
1. Copy `.env.example` to `.env` and fill values (especially TELEGRAM_BOT_TOKEN, DATABASE credentials, BASE_URL, ADMIN_API_KEY).
2. Place `models.sql` into `web/` (it's already included).
3. Build and run with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
4. Create a Telegram bot via BotFather and set TELEGRAM_BOT_TOKEN in `.env`.
5. Use a consenting test account to interact with the bot.

## Notes
- Always run behind HTTPS in production.
- Ensure explicit written authorization is obtained for each test.
- This repo is provided as code examples for ethical testing and training.
