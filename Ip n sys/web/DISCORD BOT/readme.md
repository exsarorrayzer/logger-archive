# DISCORD BOT DM SYSTEM

This system sends logs directly to your **Discord DM** (Direct Message) via a bot. You just need to provide your **Owner ID** (User ID).

## CONFIGURATION

You MUST fill in these variables at the top of each file:
- `BOT_TOKEN`: Your Bot Token from the Discord Developer Portal.
- `OWNER_ID`: Your Discord User ID (where log DMs will be sent).

## FILES

### rayzer.js (Vercel / Next.js)
- Can be used as a Next.js API route.
- Place it in the `/api/` directory.
- **Security:** Runs server-side. Your Token and Owner ID are hidden from clients.

### rayzer.php (Standard Hosting)
- Works on PHP-supported hosting (cPanel, etc.).
- Requires the `CURL` extension.

### rayzer.py (Backend Module)
- Can be integrated into Flask or FastAPI projects.
- Requires the `requests` library.

---
