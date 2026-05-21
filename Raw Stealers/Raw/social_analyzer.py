import requests
import json
import re

def analyze_social_media(cookies_list):
    results = []
    
    # Simple check for account presence and basic info using cookies
    # We mainly look for cookies that indicate a logged-in session
    socials = {
        "Twitter/X": ["auth_token", "twid"],
        "Instagram": ["sessionid", "ds_user_id"],
        "TikTok": ["sessionid", "sid_guard"],
        "Facebook": ["c_user", "xs"],
        "Reddit": ["reddit_session"]
    }
    
    found_accounts = {}
    
    for cookie in cookies_list:
        host = cookie.get('host', '')
        name = cookie.get('name', '')
        
        for social_name, key_cookies in socials.items():
            if any(x in host.lower() for x in social_name.lower().split('/')):
                if name in key_cookies:
                    if social_name not in found_accounts:
                        found_accounts[social_name] = []
                    found_accounts[social_name].append(name)

    if not found_accounts:
        return "No significant social media sessions detected in provided cookies."
        
    report = "╔════════════════════════════════════════╗\n"
    report += "║         SOCIAL MEDIA ANALYZER          ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for social, keys in found_accounts.items():
        report += f"║ {social.ljust(15)}: [LOGGED IN] {' '.join(keys)[:15]} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
