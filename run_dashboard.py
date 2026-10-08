"""
Launcher for Credit Risk Analytics & Scoring Dashboard
Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
"""

import sys
import os
import webbrowser
import threading
import time

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import uvicorn

def open_browser(url: str, delay_seconds: float = 1.2):
    """Open default browser after server initializes."""
    time.sleep(delay_seconds)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

def main():
    host = "127.0.0.1"
    port = 8088
    url = f"http://localhost:{port}"

    print("=" * 78)
    print(" CREDIT RISK INTELLIGENCE & SCORING ENGINE - WEB DASHBOARD")
    print(f" URL Local: {url}")
    print("=" * 78)

    # Launch browser in separate thread
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    # Run FastAPI via Uvicorn
    uvicorn.run("dashboard.server:app", host=host, port=port, log_level="info", reload=False)

if __name__ == "__main__":
    main()
