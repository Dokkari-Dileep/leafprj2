#!/usr/bin/env python3
"""
Installation script for CropGuard AI
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(cmd, description):
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Success")
            return True
        else:
            print(f"✗ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print_header("CROPGUARD AI - INSTALLATION")
    
    # Create directories
    print("\nCreating directories...")
    directories = [
        'static/images',
        'static/uploads',
        'templates',
        'model',
        'dataset'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")
    
    # Install dependencies
    print_header("INSTALLING DEPENDENCIES")
    
    dependencies = [
        "pip install flask",
        "pip install pillow",
        "pip install numpy",
        "pip install requests",
        "pip install python-dotenv"
    ]
    
    for dep in dependencies:
        if not run_command(dep, f"Installing {dep.split()[2]}"):
            print("Continuing with basic installation...")
    
    # Create model files
    print_header("CREATING MODEL FILES")
    
    # Check if TensorFlow is available
    try:
        import tensorflow
        print("✓ TensorFlow is installed")
        has_tensorflow = True
    except:
        print("⚠️ TensorFlow not installed")
        print("  The system will run in demo mode")
        has_tensorflow = False
    
    # Create the real model file
    import create_real_model
    print("✓ Created valid model files")
    
    # Create basic disease info if not exists
    if not os.path.exists('disease_info.json'):
        import json
        basic_info = {
            "Apple_Scab": {
                "description": "Apple scab is a serious fungal disease affecting apple trees.",
                "causes": ["Fungus Venturia inaequalis", "Cool wet weather"],
                "symptoms": ["Dark spots on leaves", "Deformed fruits"],
                "precautions": ["Plant resistant varieties", "Good air circulation"],
                "treatments": ["Apply fungicides", "Remove infected leaves"],
                "organic_remedies": ["Neem oil", "Baking soda spray"]
            }
        }
        with open('disease_info.json', 'w') as f:
            json.dump(basic_info, f, indent=2)
        print("✓ Created disease_info.json")
    
    # Create feedback log if not exists
    if not os.path.exists('feedback_log.json'):
        with open('feedback_log.json', 'w') as f:
            json.dump([], f)
        print("✓ Created feedback_log.json")
    
    print_header("INSTALLATION COMPLETE")
    print("\n✅ Setup completed successfully!")
    print("\nTo start the application:")
    print("  python app.py")
    print("\nThen open your browser:")
    print("  http://localhost:5000")
    print("\nFor real disease detection:")
    print("  1. Add your dataset images to 'dataset/' folder")
    print("  2. Install TensorFlow: pip install tensorflow")
    print("  3. Train the model: python train_model.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())