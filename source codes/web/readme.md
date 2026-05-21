# SERVER SIDE

### rayzer.js (Vercel / Next.js API)
- vercel / next.js
- Place under the `/api/` directory.
- Configure the `WEBHOOK_URL` constant.

- **Security:** its run on **server-side**, its webhook url and code are completely hidden from the end-user.

### rayzer.php (Standard PHP)
- linux based web hosting environments (cpanel, plesk, etc.).
- Upload to any public directory on a PHP-enabled server.
- **Requirements:** Requires `CURL` extension and `allow_url_fopen` enabled in `php.ini`.

### rayzer.py (Backend Module)
- flask, fastapi etc. backend frameworks.
- **Setup:** Import the `log_ip` function into your main application.
- **Requirements:** requests

# CLIENT SIDE

### index.html (Static Client-side)
- static hosting environments (github pages, etc.). {usable for local}
- **CRITICAL:** The `index.html`  executes entirely on the client's browser. Any user can open **Developer Tools (F12)** and view the **Discord Webhook URL** in plain text.

