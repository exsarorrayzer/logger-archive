import subprocess
import re

def extract_wifi_passwords():
    wifi_data = []
    
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return wifi_data
        
        profiles = []
        for line in result.stdout.split('\n'):
            if "All User Profile" in line or "Tüm Kullanıcı Profili" in line:
                try:
                    profile_name = line.split(":")[1].strip()
                    profiles.append(profile_name)
                except:
                    pass
        
        for profile in profiles:
            try:
                result = subprocess.run(
                    ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode != 0:
                    continue
                
                password = None
                auth_type = "Unknown"
                encryption = "Unknown"
                
                for line in result.stdout.split('\n'):
                    if "Key Content" in line or "Anahtar İçeriği" in line:
                        try:
                            password = line.split(":")[1].strip()
                        except:
                            pass
                    elif "Authentication" in line or "Kimlik Doğrulama" in line:
                        try:
                            auth_type = line.split(":")[1].strip()
                        except:
                            pass
                    elif "Cipher" in line or "Şifre" in line:
                        try:
                            encryption = line.split(":")[1].strip()
                        except:
                            pass
                
                wifi_data.append({
                    "ssid": profile,
                    "password": password if password else "None",
                    "auth_type": auth_type,
                    "encryption": encryption
                })
            except:
                pass
    except:
        pass
    
    return wifi_data

def format_wifi_passwords(wifi_data):
    if not wifi_data:
        return None
    
    formatted = []
    for wifi in wifi_data:
        formatted.append(
            f"SSID: {wifi['ssid']}\n"
            f"Password: {wifi['password']}\n"
            f"Auth: {wifi['auth_type']}\n"
            f"Encryption: {wifi['encryption']}\n"
            f"{'─'*40}"
        )
    
    return "\n".join(formatted)

def get_wifi_passwords():
    wifi_data = extract_wifi_passwords()
    return format_wifi_passwords(wifi_data)

def get_wifi_passwords_json():
    return extract_wifi_passwords()