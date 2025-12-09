"""
Pest Detector - CNN Model
Detects pest damage in crop images
"""

import os
import sys
import numpy as np
from PIL import Image
import cv2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# TensorFlow imports - compatible way
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    print(f"✅ TensorFlow {tf.__version__} loaded successfully!")
except ImportError as e:
    print(f"❌ TensorFlow import error: {e}")
    sys.exit(1)

from sklearn.model_selection import train_test_split

class PestDetector:
    def __init__(self):
        self.model = None
        self.img_size = (64, 64)
        self.model_path = os.path.join(Config.MODEL_DIR, 'pest_detector.h5')
        
        os.makedirs(Config.MODEL_DIR, exist_ok=True)
        os.makedirs(Config.DATA_UPLOADS, exist_ok=True)
    
    def create_model(self):
        """Create a simple CNN for binary classification"""
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("✅ Model created successfully!")
        return model
    
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic training data"""
        print(f"🎨 Generating {n_samples} synthetic training samples...")
        
        X = []
        y = []
        
        for i in range(n_samples):
            img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
            label = np.random.randint(0, 2)
            
            if label == 1:  # Damaged
                for _ in range(5):
                    x_pos = np.random.randint(10, 54)
                    y_pos = np.random.randint(10, 54)
                    cv2.circle(img, (x_pos, y_pos), 3, (50, 30, 20), -1)
            else:  # Healthy
                img[:, :, 1] = np.clip(img[:, :, 1] + 50, 0, 255)
            
            X.append(img / 255.0)
            y.append(label)
        
        print("✅ Synthetic data generated!")
        return np.array(X), np.array(y)
    
    def train_model(self, epochs=5):
        """Train the model"""
        if self.model is None:
            self.create_model()
        
        X, y = self.generate_synthetic_data(n_samples=1000)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"\n🚀 Training model...")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Validation samples: {len(X_val)}")
        
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=1
        )
        
        self.model.save(self.model_path)
        print(f"\n✅ Model saved to: {self.model_path}")
        return history
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            self.model = models.load_model(self.model_path)
            print(f"✅ Model loaded from: {self.model_path}")
            return True
        return False
    
    def predict_image(self, image_path):
        """Predict if image shows pest damage"""
        if self.model is None:
            if not self.load_model():
                return None
        
        img = Image.open(image_path).resize(self.img_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = self.model.predict(img_array, verbose=0)[0][0]
        
        return {
            'pest_probability': float(prediction),
            'classification': 'Damaged' if prediction > 0.5 else 'Healthy'
        }


if __name__ == "__main__":
    print("=" * 60)
    print("🐛 Pest Detector CNN - Training & Testing")
    print("=" * 60)
    
    detector = PestDetector()
    
    print("\n[Step 1] Creating model...")
    detector.create_model()
    detector.model.summary()
    
    print("\n[Step 2] Training model (5 epochs)...")
    history = detector.train_model(epochs=5)
    
    print("\n[Step 3] Testing model...")
    test_img = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    test_path = os.path.join(Config.DATA_UPLOADS, 'test_crop.png')
    Image.fromarray(test_img).save(test_path)
    
    result = detector.predict_image(test_path)
    print(f"\n📊 Test Result:")
    print(f"   Pest Probability: {result['pest_probability']:.2%}")
    print(f"   Classification: {result['classification']}")
    
    print("\n" + "=" * 60)
    print("✅ Pest Detector Ready!")
    print("=" * 60)