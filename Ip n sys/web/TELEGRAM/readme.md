# TELEGRAM BOT SYSTEM

This system sends logs to your **Telegram Bot**.

## CONFIGURATION

You MUST fill in these variables at the top of each file:
- `BOT_TOKEN`: Your Telegram Bot Token from @BotFather.
- `CHAT_ID`: Your Telegram User ID or Group ID.

## FILES

### rayzer.js (Vercel / Next.js)
- Can be used as a Next.js API route.
- Place it in the `/api/` directory.
- **Security:** Runs server-side. Your Token and Chat ID are hidden from clients.

### rayzer.php (Standard Hosting)
- Works on PHP-supported hosting (cPanel, etc.).
- Requires the `CURL` extension.

### rayzer.py (Backend Module)
- Can be integrated into Flask or FastAPI projects.
- Requires the `requests` library.

---
**Rayzer Logger System**
