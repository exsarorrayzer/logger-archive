# CLOUDFLARE WORKER - DISCORD BOT DM

This system uses Cloudflare Workers to send logs directly to your **Discord DM** (Direct Message) via a bot.

## CONFIGURATION

You MUST fill in these variables:
- `BOT_TOKEN`: Your Bot Token from the Discord Developer Portal.
- `OWNER_ID`: Your Discord User ID (where logs will be sent).

## SETUP

### 1. Hardcoded Version (worker-hardcoded.js)
- Edit the variables directly in the code.
- **Risk:** Bot Token exposure if the source code is leaked.

### 2. Environment Variables Version
- You can adapt the `worker-env.js` to use `BOT_TOKEN` and `OWNER_ID` as secrets.

---
**Rayzer Logger System**
