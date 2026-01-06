import os
import numpy as np
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import cv2
from PIL import Image

class DiseaseDetectionModel:
    def __init__(self, data_dir='dataset/train', img_size=(224, 224)):
        self.data_dir = data_dir
        self.img_size = img_size
        self.class_names = []
        self.model = None
        self.disease_info = {}
        
    def load_dataset(self):
        """Load and organize dataset"""
        images = []
        labels = []
        
        print("📂 Loading dataset...")
        
        for class_name in os.listdir(self.data_dir):
            class_dir = os.path.join(self.data_dir, class_name)
            if os.path.isdir(class_dir):
                self.class_names.append(class_name)
                
                # Load each image in class directory
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(class_dir, img_name)
                        try:
                            # Load and preprocess image
                            img = Image.open(img_path)
                            img = img.resize(self.img_size)
                            img_array = np.array(img)
                            
                            # Normalize pixel values
                            img_array = img_array / 255.0
                            
                            images.append(img_array)
                            labels.append(class_name)
                            
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
        
        images = np.array(images)
        labels = np.array(labels)
        
        print(f"✅ Loaded {len(images)} images across {len(self.class_names)} classes")
        return images, labels
    
    def encode_labels(self, labels):
        """Convert string labels to numerical"""
        self.label_encoder = LabelEncoder()
        encoded_labels = self.label_encoder.fit_transform(labels)
        return encoded_labels
    
    def create_model(self, num_classes):
        """Create CNN model for disease detection"""
        model = Sequential([
            # First convolutional block
            Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(*self.img_size, 3)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Second convolutional block
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Third convolutional block
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Fourth convolutional block
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            # Fully connected layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        
        return model
    
    def train(self, epochs=50, batch_size=32):
        """Train the model"""
        # Load data
        images, labels = self.load_dataset()
        
        # Encode labels
        encoded_labels = self.encode_labels(labels)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            images, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
        )
        
        # Create model
        self.model = self.create_model(len(self.class_names))
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Callbacks
        callbacks = [
            EarlyStopping(patience=10, restore_best_weights=True),
            ModelCheckpoint('best_model.h5', save_best_only=True),
            ReduceLROnPlateau(factor=0.5, patience=5, min_lr=0.00001)
        ]
        
        # Data augmentation
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest'
        )
        
        # Train model
        print("🚀 Training model...")
        history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            validation_data=(X_val, y_val),
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        val_loss, val_acc = self.model.evaluate(X_val, y_val, verbose=0)
        print(f"\n✅ Training completed!")
        print(f"📊 Validation Accuracy: {val_acc:.4f}")
        print(f"📊 Validation Loss: {val_loss:.4f}")
        
        return history
    
    def save_model(self, model_path='disease_model.h5'):
        """Save trained model and class names"""
        # Save model
        self.model.save(model_path)
        print(f"✅ Model saved to {model_path}")
        
        # Save class names
        with open('class_names.pkl', 'wb') as f:
            pickle.dump(self.class_names, f)
        print("✅ Class names saved")
        
        # Create disease information
        self.create_disease_info()
        
        # Save disease information
        with open('disease_info.json', 'w') as f:
            json.dump(self.disease_info, f, indent=4)
        print("✅ Disease information saved")
    
    def create_disease_info(self):
        """Create comprehensive disease information"""
        disease_treatments = {
            # Apple diseases
            "Apple_Scab": {
                "symptoms": "Olive-green to black spots on leaves, fruits become corky",
                "treatment": "Apply fungicides containing myclobutanil or trifloxystrobin",
                "prevention": "Remove fallen leaves, prune for air circulation",
                "chemical_control": "Captan, Mancozeb, Sulfur-based fungicides",
                "organic_control": "Neem oil, Baking soda spray, Copper fungicide"
            },
            "Apple_Black_Rot": {
                "symptoms": "Brown spots on leaves, black rot on fruits",
                "treatment": "Remove infected parts, apply fungicide sprays",
                "prevention": "Proper pruning, avoid wounding fruits",
                "chemical_control": "Thiophanate-methyl, Propiconazole",
                "organic_control": "Sulfur dust, Copper sprays"
            },
            "Apple_Cedar_apple_rust": {
                "symptoms": "Orange-yellow spots on leaves, galls on junipers",
                "treatment": "Apply fungicides in early spring",
                "prevention": "Remove nearby juniper plants",
                "chemical_control": "Myclobutanil, Triadimefon",
                "organic_control": "Sulfur, Copper fungicides"
            },
            "Apple_Healthy": {
                "symptoms": "No disease symptoms present",
                "treatment": "Maintain current care practices",
                "prevention": "Regular monitoring, balanced fertilization",
                "chemical_control": "Not required",
                "organic_control": "Continue organic practices"
            },
            # Tomato diseases
            "Tomato_Early_blight": {
                "symptoms": "Dark spots with concentric rings on leaves",
                "treatment": "Remove infected leaves, apply fungicides",
                "prevention": "Crop rotation, proper spacing",
                "chemical_control": "Chlorothalonil, Mancozeb",
                "organic_control": "Copper fungicide, Baking soda spray"
            },
            "Tomato_Late_blight": {
                "symptoms": "Water-soaked spots, white mold under leaves",
                "treatment": "Immediate removal of infected plants",
                "prevention": "Avoid overhead watering",
                "chemical_control": "Metalaxyl, Mancozeb",
                "organic_control": "Copper fungicides, Remove infected plants"
            },
            "Tomato_Healthy": {
                "symptoms": "No disease symptoms present",
                "treatment": "Maintain current care practices",
                "prevention": "Regular pruning, proper watering",
                "chemical_control": "Not required",
                "organic_control": "Neem oil preventive sprays"
            },
            # Potato diseases
            "Potato_Early_blight": {
                "symptoms": "Brown spots with target-like rings on leaves",
                "treatment": "Apply fungicides at first sign",
                "prevention": "Crop rotation, remove plant debris",
                "chemical_control": "Chlorothalonil, Azoxystrobin",
                "organic_control": "Copper fungicide, Bacillus subtilis"
            },
            "Potato_Late_blight": {
                "symptoms": "Black lesions on leaves and stems",
                "treatment": "Destroy infected plants immediately",
                "prevention": "Use certified seed potatoes",
                "chemical_control": "Mancozeb, Metalaxyl-M",
                "organic_control": "Copper sprays, Remove infected plants"
            },
            # Grape diseases
            "Grape_Black_rot": {
                "symptoms": "Brown spots on leaves, black mummies on fruits",
                "treatment": "Apply fungicides during growing season",
                "prevention": "Proper pruning, remove infected fruits",
                "chemical_control": "Myclobutanil, Tebuconazole",
                "organic_control": "Sulfur, Copper sprays"
            },
            # Add more disease information as needed...
        }
        
        # Create info for all classes
        for class_name in self.class_names:
            if class_name in disease_treatments:
                self.disease_info[class_name] = disease_treatments[class_name]
            else:
                # Default information for other diseases
                self.disease_info[class_name] = {
                    "symptoms": f"Specific symptoms for {class_name.replace('_', ' ')}",
                    "treatment": "Consult local agricultural extension officer",
                    "prevention": "Maintain plant health, regular monitoring",
                    "chemical_control": "Appropriate fungicide as recommended",
                    "organic_control": "Neem oil, copper sprays, proper sanitation"
                }

def main():
    # Initialize and train model
    trainer = DiseaseDetectionModel(data_dir='dataset/train', img_size=(224, 224))
    
    # Train model
    trainer.train(epochs=30, batch_size=32)
    
    # Save model and resources
    trainer.save_model('disease_model.h5')
    
    print("\n🎉 Model training completed successfully!")
    print(f"Total classes trained: {len(trainer.class_names)}")

if __name__ == "__main__":
    main()