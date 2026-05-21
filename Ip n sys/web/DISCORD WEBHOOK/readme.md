# DISCORD WEBHOOK SYSTEM

This system sends logs to your specified **Discord Webhook URL**.

## CONFIGURATION

You MUST fill in this variable at the top of each file:
- `WEBHOOK_URL`: Your Discord Webhook URL.

## FILES

### rayzer.js (Vercel / Next.js)
- Can be used as a Next.js API route.
- Place it in the `/api/` directory.
- **Security:** Runs server-side. Your Webhook URL is hidden from clients.

### rayzer.php (Standard Hosting)
- Works on PHP-supported hosting (cPanel, etc.).
- Requires the `CURL` extension.

### rayzer.py (Backend Module)
- Can be integrated into Flask or FastAPI projects.
- Requires the `requests` library.

### index.html (WARNING)
- **CRITICAL:** Executes client-side. Anyone can see your **Webhook URL** via F12 (Developer Tools).

---
**Rayzer Logger System**
