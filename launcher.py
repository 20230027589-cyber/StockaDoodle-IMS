# launcher.py - StockaDoodle One-Click Launcher

# Icon: desktop_app/assets/icons/stockadoodle-white.ico

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# Change this if your UI entry point is different
UI_SCRIPT = "desktop_app/main.py"        # ← change if needed
API_SCRIPT = "api_server/app.py"

def start_api_server():
    """Start Flask API in background (completely hidden on Windows)"""
    cmd = [sys.executable, API_SCRIPT]
    if sys.platform == "win32":
        # Hide console window completely
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen(
            cmd,
            creationflags=CREATE_NO_WINDOW,
            cwd=Path(__file__).parent
        )
    else:
        subprocess.Popen(cmd, cwd=Path(__file__).parent)

def wait_for_api(timeout=30):
    """Wait until /health endpoint responds"""
    import requests
    url = "http://127.0.0.1:5000/api/v1/health"
    for _ in range(timeout):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except:
            time.sleep(1)
    return False

def main():
    print("Starting StockaDoodle IMS...")
    start_api_server()
    
    print("Waiting for API server...")
    if not wait_for_api():
        input("Failed to start API server. Press Enter to exit...")
        return
    
    print("Launching desktop app...")
    # Launch your PyQt UI
    os.system(f'"{sys.executable}" "{UI_SCRIPT}"')

if __name__ == "__main__":
    main()

