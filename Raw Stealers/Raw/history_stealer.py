import os
import sqlite3
import tempfile
import shutil
from .utils import get_all_browser_profiles, load_json_config, expand_path

def extract_history_data():
    history_report = []
    bookmarks_report = []
    search_history = []
    
    browser_config = load_json_config("browser.json")
    
    for browser in browser_config.get("chromium_browsers", []):
        browser_path = expand_path(browser["path"])
        browser_name = browser["name"]
        
        if not os.path.exists(browser_path):
            continue
            
        profiles = get_all_browser_profiles(browser_path)
        for profile in profiles:
            history_db = os.path.join(browser_path, profile, "History")
            if os.path.exists(history_db):
                temp_history = os.path.join(tempfile.gettempdir(), f"History_{browser_name}_{profile}_{os.getpid()}")
                try:
                    shutil.copy2(history_db, temp_history)
                    conn = sqlite3.connect(temp_history)
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                    for row in cursor.fetchall():
                        history_report.append(f"[{browser_name}|{profile}] {row[1][:50]} -> {row[0][:100]}")
                    
                    try:
                        cursor.execute("SELECT term FROM keyword_search_terms LIMIT 100")
                        for row in cursor.fetchall():
                            search_history.append(f"[{browser_name}] Search: {row[0]}")
                    except: pass
                    
                    cursor.close()
                    conn.close()
                except: pass
                finally:
                    if os.path.exists(temp_history): os.remove(temp_history)
            
            bookmarks_path = os.path.join(browser_path, profile, "Bookmarks")
            if os.path.exists(bookmarks_path):
                try:
                    import json
                    with open(bookmarks_path, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                        def parse_bookmarks(nodes):
                            for node in nodes:
                                if node['type'] == 'url':
                                    bookmarks_report.append(f"[{browser_name}] {node['name']} -> {node['url']}")
                                elif node['type'] == 'folder':
                                    parse_bookmarks(node['children'])
                        
                        if 'roots' in data:
                            for root in data['roots'].values():
                                if 'children' in root:
                                    parse_bookmarks(root['children'])
                except: pass
                
    return history_report, bookmarks_report, search_history

def get_history_report():
    h, b, s = extract_history_data()
    if not h and not b and not s: return None
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║        HISTORY & BOOKMARKS REPORT       ║\n"
    report += "╠════════════════════════════════════════╣\n"
    
    report += "║ --- TOP SEARCHES ---\n"
    for item in s[:20]: report += f"║ {item[:38].ljust(38)} ║\n"
    
    report += "╠════════════════════════════════════════╣\n"
    report += "║ --- TOP BOOKMARKS ---\n"
    for item in b[:30]: report += f"║ {item[:38].ljust(38)} ║\n"
    
    report += "╠════════════════════════════════════════╣\n"
    report += "║ --- LATEST HISTORY ---\n"
    for item in h[:50]: report += f"║ {item[:38].ljust(38)} ║\n"
    
    report += "╚════════════════════════════════════════╝"
    return report
