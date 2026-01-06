# run.py
import os
import sys
import webbrowser
from threading import Timer
import subprocess

def run_application():
    """Run the Flask application"""
    print("🚀 Starting AgriDetect Application...")
    print("-" * 50)
    
    # Check if required files exist
    required_files = ['app.py', 'config.py', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            print("Please run setup.py first")
            return False
    
    # Open browser after 3 seconds
    def open_browser():
        webbrowser.open('http://localhost:5000')
    
    Timer(3, open_browser).start()
    
    # Run the Flask application
    try:
        print("Starting Flask server...")
        print("Open your browser to: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run Flask app
        os.system('python app.py')
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_application()