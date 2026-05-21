import winreg
import json

def get_installed_apps():
    apps = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
    ]
    
    for hkey, path in reg_paths:
        try:
            with winreg.OpenKey(hkey, path) as key:
                num_subkeys = winreg.QueryInfoKey(key)[0]
                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                apps.append({"name": name, "version": version})
                            except: pass
                    except: pass
        except: pass
    
    # Remove duplicates and sort
    unique_apps = []
    seen = set()
    for app in apps:
        if app['name'] not in seen:
            unique_apps.append(app)
            seen.add(app['name'])
            
    return sorted(unique_apps, key=lambda x: x['name'])

def get_apps_report():
    apps = get_installed_apps()
    if not apps:
        return "No installed applications found."
        
    report = "╔════════════════════════════════════════╗\n"
    report += "║         INSTALLED APPLICATIONS         ║\n"
    report += "╠════════════════════════════════════════╣\n"
    for app in apps:
        report += f"║ {str(app['name'])[:37].ljust(38)} ║\n"
    report += "╚════════════════════════════════════════╝"
    return report
