#!/usr/bin/env python3
"""
Simple script to run all Streamlit apps on different ports
"""

import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def run_streamlit_app(app_path, port):
    """Run a Streamlit app on a specific port"""
    cmd = [
        "streamlit", "run", str(app_path),
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running app {app_path} on port {port}: {e}")
    except KeyboardInterrupt:
        print(f"Stopping app {app_path}")

def main():
    """Main function to run all apps"""
    
    # Define apps and their ports
    apps = [
        {
            "name": "Stock Dashboard",
            "path": Path("streamlit_apps/stock_dashboard/app.py"),
            "port": 8501,
            "url": "http://localhost:8501"
        },
        {
            "name": "Text Analyzer", 
            "path": Path("streamlit_apps/text_analyzer/app.py"),
            "port": 8502,
            "url": "http://localhost:8502"
        },
        {
            "name": "Weather Predictor",
            "path": Path("streamlit_apps/weather_predictor/app.py"),
            "port": 8503,
            "url": "http://localhost:8503"
        }
    ]
    
    print("🚀 Starting Streamlit Portfolio Apps")
    print("=" * 50)
    
    # Check if app files exist
    for app in apps:
        if not app["path"].exists():
            print(f"❌ Error: {app['path']} not found!")
            return
    
    print("📋 Apps to start:")
    for app in apps:
        print(f"  • {app['name']}: {app['url']}")
    print()
    
    # Start apps in separate threads
    threads = []
    
    for app in apps:
        print(f"🏃 Starting {app['name']} on port {app['port']}...")
        thread = threading.Thread(
            target=run_streamlit_app,
            args=(app["path"], app["port"]),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        time.sleep(2)  # Give each app time to start
    
    print("\n✅ All apps started!")
    print("\n🌐 Your apps are running at:")
    for app in apps:
        print(f"  • {app['name']}: {app['url']}")
    
    print("\n📖 Portfolio website: Open index.html in your browser")
    print("\n💡 Tips:")
    print("  • Update config.json to customize your portfolio")
    print("  • Press Ctrl+C to stop all apps")
    print("  • Each app runs independently on its own port")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all apps...")
        return

if __name__ == "__main__":
    main() 