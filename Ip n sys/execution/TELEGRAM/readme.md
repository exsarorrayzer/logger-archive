# TELEGRAM BOT SYSTEM (EXECUTION)

This system sends logs from the victim's machine directly to your **Telegram Bot**.

## CONFIGURATION

You MUST fill in these variables at the top of each file:
- `BOT_TOKEN`: Your Telegram Bot Token from @BotFather.
- `CHAT_ID`: Your Telegram User ID or Group ID.

## FILES

### rayzer.py (Python Script)
- Works on Windows, Linux, and macOS.
- **Requirements:** Requires the `requests` library.

### rayzer.bat (Windows Batch)
- Works on Windows systems.
- Uses PowerShell to send the log via Telegram Bot API.

### rayzer.sh (Linux Bash)
- Works on Linux/Unix systems.
- **Requirements:** Requires `curl` to be installed.

---
**Rayzer Logger System**
