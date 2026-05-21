# CLOUDFLARE WORKER - DISCORD WEBHOOK

This system uses Claudflare Workers to log IP addresses and send them to a **Discord Webhook**.

## FILES

### 1. worker-hardcoded.js
- The Webhook URL is defined as a constant within the code.
- **Risk:** Sharing the source code exposes your Webhook URL.

### 2. worker-env.js
- Pulls configuration from Cloudflare's environment variables (Secrets).
- **Setup:**
  1. Go to your Worker in the Cloudflare Dashboard.
  2. Navigate to `Settings` -> `Variables`.
  3. Add `WEBHOOK_URL` as a secret variable.
  4. (Optional) Add `GIF_URL` as a secret variable.

---
**Rayzer Logger System**
