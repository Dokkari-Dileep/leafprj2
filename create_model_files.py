#!/usr/bin/env python3
"""
Create model files for Multi-Crop Disease Detection
This script creates the necessary model files for the system to work
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def create_class_names():
    """Create class_names.json file"""
    class_names = [
        "Apple_Scab", "Apple_Black_Rot", "Apple_Cedar_apple_rust", "Apple_Healthy",
        "Cherry_Healthy", "Cherry_Brightness_Adjusted", "Cherry_Constrast_Adjusted", 
        "Cherry_Flipped_Horizontal", "Cherry_Flipped_Vertical", "Corn_Common_rust",
        "Corn_Northern_Leaf_Blight", "Corn_Healthy", "Grape_Black_rot", "Grape_Esca",
        "Grape_Leaf_blight", "Grape_Healthy", "Peach_Bacterial_spot", "Peach_Healthy",
        "Pepper_bell_Bacterial_spot", "Pepper_bell_Healthy", "Potato_Early_blight",
        "Potato_Late_blight", "Potato_Healthy", "Strawberry_Leaf_scorch", "Strawberry_Healthy",
        "Tomato_Early_blight", "Tomato_Late_blight", "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
        "Tomato_Spider_mites", "Tomato_Healthy", "watermelon_Anthraconse", "watermelon_Downy_mildew",
        "watermelon_Healthy", "watermelon_Virus", "Pomegrante_Alternaria", "Pomegrante_Anthraconse",
        "Pomegrante_Bacterail_Blight", "Pomegrante_Cercospora", "Pomegrante_Healthy",
        "Eggplant_Healthy", "Eggplant_Insect_Pest", "Eggplant_LeafSpot", "Eggplant_White_Mold",
        "Custard_Apple_Anthracnose", "Custard_Apple_Blank_Canker", "Custard_Apple_Diplodia_rot",
        "Custard_Apple_Leaf_Spot_on_Leaves", "Custard_Apple_Mealy_Bug", "Leamon_Healthy",
        "Leamon_Spider_Mites", "Leamon_Sooty_Mould", "Leamon_Curl_Virus", "Leamon_Anthraconse"
    ]
    
    # Ensure model directory exists
    os.makedirs('model', exist_ok=True)
    
    # Save class names
    with open('model/class_names.json', 'w') as f:
        json.dump(class_names, f, indent=2)
    
    print(f"✓ Created class_names.json with {len(class_names)} classes")
    return class_names

def create_dummy_model():
    """Create a dummy model file for demonstration"""
    model_content = """This is a placeholder model file.
    
For actual disease detection, you need to:
1. Install TensorFlow: pip install tensorflow==2.13.0
2. Add your dataset images to the 'dataset' folder
3. Run the training script: python train_model.py

The training script will create a real model.h5 file.

For now, the system runs in demo mode with sample predictions.
"""
    
    with open('model/disease_model.h5', 'w') as f:
        f.write(model_content)
    
    print("✓ Created dummy disease_model.h5")
    print("⚠️ Note: This is a placeholder. Train with your dataset for real predictions.")

def create_training_history():
    """Create a sample training history plot"""
    try:
        # Create sample training data
        epochs = range(1, 31)
        train_acc = [0.2 + i*0.025 for i in range(30)]
        val_acc = [0.15 + i*0.023 for i in range(30)]
        train_loss = [2.0 - i*0.06 for i in range(30)]
        val_loss = [2.2 - i*0.055 for i in range(30)]
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(epochs, train_acc, 'b-', label='Training Accuracy')
        ax1.plot(epochs, val_acc, 'r-', label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot loss
        ax2.plot(epochs, train_loss, 'b-', label='Training Loss')
        ax2.plot(epochs, val_loss, 'r-', label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model/training_history.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        print("✓ Created training_history.png")
        
    except Exception as e:
        print(f"⚠️ Could not create training history plot: {e}")
        # Create a simple text file instead
        with open('model/training_history.png', 'w') as f:
            f.write("Training history plot would be generated during actual training.")

def create_dataset_structure():
    """Create the dataset directory structure"""
    class_names = create_class_names()
    
    # Create dataset directory
    os.makedirs('dataset', exist_ok=True)
    
    # Create README file
    readme_content = """# Dataset Directory Structure

This directory should contain your crop disease images organized as follows:

dataset/
├── Apple_Scab/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Apple_Black_Rot/
│   └── ...
├── Apple_Cedar_apple_rust/
│   └── ...
└── ... (other disease folders)

Requirements:
1. Each disease should have its own folder named exactly as in class_names.json
2. Images should be in JPG, PNG, or JPEG format
3. Minimum 100 images per class for good results
4. Image size should be at least 224x224 pixels
5. Include both healthy and diseased samples

You can download sample datasets from:
- PlantVillage Dataset: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- PlantDoc Dataset: https://github.com/pratikkayal/PlantDoc-Dataset
- Create your own by photographing crop leaves

After adding your images, run: python train_model.py
"""
    
    with open('dataset/README.txt', 'w') as f:
        f.write(readme_content)
    
    # Create placeholder folders
    created_folders = 0
    for class_name in class_names[:10]:  # Create first 10 as example
        folder_path = os.path.join('dataset', class_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create README in each folder
        folder_readme = f"""# {class_name.replace('_', ' ')}

Place your {class_name.replace('_', ' ')} images in this folder.

Image requirements:
- Format: JPG, PNG, JPEG
- Size: Minimum 224x224 pixels
- Quality: Clear, well-lit images
- Quantity: At least 100 images recommended

Naming convention: image_001.jpg, image_002.jpg, etc.
"""
        
        with open(os.path.join(folder_path, 'README.txt'), 'w') as f:
            f.write(folder_readme)
        
        created_folders += 1
    
    print(f"✓ Created dataset structure with {created_folders} sample folders")
    print("⚠️ Note: Add your actual images to these folders for training")

def create_sample_images():
    """Create sample images for the static folder"""
    os.makedirs('static/images', exist_ok=True)
    
    # Create simple colored backgrounds
    colors = {
        'bg-home': (240, 248, 255),  # Alice Blue
        'bg-dataset': (230, 242, 255),  # Light Blue
        'bg-feedback': (255, 248, 225),  # Light Yellow
        'bg-result': (225, 248, 240),  # Light Mint
        'bg-tutorial': (245, 245, 245)   # Light Gray
    }
    
    for name, color in colors.items():
        # Create a simple colored image
        img = Image.new('RGB', (800, 600), color)
        
        # Add a subtle pattern
        draw = ImageDraw.Draw(img)
        for i in range(0, 800, 40):
            draw.line([(i, 0), (i, 600)], fill=(255, 255, 255, 50), width=1)
        for i in range(0, 600, 40):
            draw.line([(0, i), (800, i)], fill=(255, 255, 255, 50), width=1)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        text = name.replace('bg-', '').replace('-', ' ').title()
        draw.text((400, 300), text, font=font, fill=(100, 100, 100, 100), anchor="mm")
        
        img.save(f'static/images/{name}.jpg', 'JPEG', quality=85)
        print(f"✓ Created: static/images/{name}.jpg")
    
    # Create logo
    logo = Image.new('RGBA', (200, 200), (40, 167, 69, 255))
    draw = ImageDraw.Draw(logo)
    
    # Draw leaf shape
    draw.ellipse((50, 50, 150, 150), fill=(255, 255, 255, 200))
    draw.ellipse((70, 70, 130, 130), fill=(40, 167, 69, 255))
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((100, 100), "CG", font=font, fill=(255, 255, 255, 255), anchor="mm")
    
    logo.save('static/images/logo.png', 'PNG')
    print("✓ Created: static/images/logo.png")

def main():
    """Main function to create all model files"""
    print("\n" + "="*60)
    print("  Creating Model Files for CropGuard AI")
    print("="*60)
    
    try:
        create_class_names()
        create_dummy_model()
        create_training_history()
        create_dataset_structure()
        create_sample_images()
        
        print("\n" + "="*60)
        print("  ✓ MODEL FILES CREATED SUCCESSFULLY")
        print("="*60)
        print("\nFiles created:")
        print("1. model/class_names.json - List of all disease classes")
        print("2. model/disease_model.h5 - Placeholder model file")
        print("3. model/training_history.png - Sample training history")
        print("4. dataset/ structure - Organized folders for your images")
        print("5. static/images/ - Background images and logo")
        
        print("\n⚠️ IMPORTANT:")
        print("For actual disease detection, you need to:")
        print("1. Add your dataset images to the 'dataset' folder")
        print("2. Install TensorFlow: pip install tensorflow==2.13.0")
        print("3. Train the model: python train_model.py")
        print("\nFor now, the system will run in demo mode.")
        
    except Exception as e:
        print(f"\n❌ Error creating model files: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())