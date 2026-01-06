# install_deps.py
import subprocess
import sys

packages = [
    "flask>=2.3.0",
    "flask-cors>=4.0.0",
    "numpy>=1.24.0",
    "pillow>=10.0.0",
    "scikit-learn>=1.3.0",
    "pandas>=2.0.0",
    "opencv-python>=4.8.0",
]

print("Installing dependencies...")
for package in packages:
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Warning: Could not install {package}: {e}")
        print("Trying with --user flag...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        except:
            print(f"Failed to install {package}")

print("✅ Basic dependencies installed!")
print("\nNote: TensorFlow is not included as it might be heavy.")
print("If you need it, run: pip install tensorflow==2.13.0")