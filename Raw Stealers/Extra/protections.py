import psutil
import os
import sys

VM_FILES = [
    "C:\\windows\\system32\\vmGuestLib.dll",
    "C:\\windows\\system32\\vm3dgl.dll",
    "C:\\windows\\system32\\vboxhook.dll",
    "C:\\windows\\system32\\vboxmrxnp.dll",
    "C:\\windows\\system32\\vmsrvc.dll",
    "C:\\windows\\system32\\drivers\\vmsrvc.sys"
]

BLACKLISTED_PROCESSES = [
    'vmtoolsd.exe', 'vmwaretray.exe', 'vmwareuser.exe', 'fakenet.exe', 'dumpcap.exe',
    'httpdebuggerui.exe', 'wireshark.exe', 'fiddler.exe', 'vboxservice.exe', 'df5serv.exe',
    'vboxtray.exe', 'ida64.exe', 'ollydbg.exe', 'pestudio.exe', 'vgauthservice.exe',
    'vmacthlp.exe', 'x96dbg.exe', 'x32dbg.exe', 'prl_cc.exe', 'prl_tools.exe',
    'xenservice.exe', 'qemu-ga.exe', 'joeboxcontrol.exe', 'ksdumperclient.exe',
    'ksdumper.exe', 'joeboxserver.exe', 'processhacker.exe', 'autoruns.exe',
    'autorunsc.exe', 'filemon.exe', 'procmon.exe', 'regmon.exe', 'procexp.exe',
    'idaq.exe', 'idaq64.exe', 'immunitydebugger.exe', 'wireshark.exe',
    'tcpview.exe', 'tempcleaner.exe', 'anyrun.exe', 'ghidra.exe', 'apimonitor.exe',
    'dnspy.exe', 'windbg.exe', 'processhacker.exe'
]

def is_vm():
    for file_path in VM_FILES:
        if os.path.exists(file_path):
            return True
    return False

def is_debugger():
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower() in BLACKLISTED_PROCESSES:
                return True
        except:
            pass
    return False

def protection_check():
    return is_vm() or is_debugger()

def is_process_running(exe_name):
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower() == exe_name.lower():
                return True
        except:
            pass
    return False

def kill_process(exe_name):
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower() == exe_name.lower():
                process.kill()
        except:
            pass

def exit_if_protected():
    if protection_check():
        sys.exit(0)