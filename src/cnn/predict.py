import tensorflow as tf
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
import cv2

class TumorDetector:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.img_size = (150, 150)  
        self.class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']
        
    def preprocess_image(self, image_url):
        """Download and preprocess image from URL"""
        try:
            # Download image from Cloudinary
            response = requests.get(image_url)
            if response.status_code != 200:
                return None
                
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed (MRI images are often grayscale)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Resize image to match model input
            img = img.resize(self.img_size)
            
            # Convert to array and normalize (same as training)
            img_array = np.array(img) / 255.0
            
            # Check if the image has the correct dimensions
            if img_array.shape != (150, 150, 3):
                # Convert grayscale to RGB if needed
                if len(img_array.shape) == 2:
                    img_array = np.stack((img_array,) * 3, axis=-1)
                else:
                    # Handle other cases as needed
                    return None
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_url):
        """Predict tumor type from image URL"""
        processed_image = self.preprocess_image(image_url)
        
        if processed_image is None:
            return {"error": "Could not process image. Please check the image URL and format."} 
        
        try:
            # Make prediction
            prediction = self.model.predict(processed_image)
            
            # Get the predicted class and confidence
            predicted_class_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class_idx])
            tumor_type = self.class_names[predicted_class_idx]
            has_tumor = tumor_type != 'notumor'
            
            # Get probabilities for all classes
            probabilities = {
                'glioma': float(prediction[0][0]),
                'meningioma': float(prediction[0][1]),
                'notumor': float(prediction[0][2]),
                'pituitary': float(prediction[0][3])
            }
            
            return {
                "has_tumor": has_tumor,
                "tumor_type": tumor_type,
                "confidence": confidence,
                "probabilities": probabilities
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return {"error": f"Prediction failed: {str(e)}"}

# Initialize the model
model_path = os.path.join(os.path.dirname(__file__), 'brain_tumor_cnn_tuned.h5')

# Check if model exists before loading
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

try:
    tumor_detector = TumorDetector(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    # Create a dummy detector for development
    class DummyDetector:
        def predict(self, image_url):
            return {"error": "Model failed to load. Please check the model file."}
    tumor_detector = DummyDetector()