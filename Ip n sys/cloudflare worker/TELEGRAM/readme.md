# CLOUDFLARE WORKER - TELEGRAM BOT

This system uses Cloudflare Workers to log IP addresses and send them to your **Telegram Bot**.

## CONFIGURATION

You MUST fill in these variables:
- `BOT_TOKEN`: Your Telegram Bot Token from @BotFather.
- `CHAT_ID`: Your Telegram User ID.

## SETUP

### 1. Hardcoded Version (worker-hardcoded.js)
- Edit the variables directly in the code.
- **Risk:** Source code exposure means Bot Token exposure.

### 2. Environment Variables Version
- You can adapt the `worker-env.js` from the Discord folder to use `BOT_TOKEN` and `CHAT_ID` as secrets.

---
**Rayzer Logger System**
