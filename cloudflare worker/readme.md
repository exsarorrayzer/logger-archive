### 1. worker-hardcoded.js
- The Webhook URL is defined as a constant within the code.
- **Risk:** Sharing the source code exposes the backend infrastructure (Webhook URL).

### 2. worker-env.js
- Pulls configuration from Cloudflare's environment variables.
- **Usage:**
  1. Navigate to your Worker in the Cloudflare Dashboard.
  2. Go to `Settings` -> `Variables`.
  3. Add `WEBHOOK_URL` as a secret variable.
  OPTIONAL: add `GIF_URL` as a secret variable and put gif url in it. else it will use default gif url inside the code.

