This directory contains payloads designed for local execution on target Windows and Linux systems.

### 1. rayzer.py
- **Conversion to Binary:** To execute on systems without a Python interpreter:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile --noconsole rayzer.py
  ```

### 2. rayzer.bat
- **Execution:** Runs via standard CMD/PowerShell.

### 3. rayzer.sh
- **Requirements:** curl
- **Execution:** `chmod +x rayzer.sh && ./rayzer.sh`

make sure you configure the config variables in the files before using them.
make sure you obfuscated the code before using them. else way antivirus software will detect them or any user can track the webhook url.
