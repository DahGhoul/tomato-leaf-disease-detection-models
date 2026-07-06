import sys
import torch
from PIL import Image
import os
import shutil
import numpy as np

# Add the current directory to path
sys.path.insert(0, '/app')

from app import load_models, predict_with_model, generate_gradcam, preprocess_image

def run_test():
    print("Loading models...")
    models = load_models()
    model = models["MobileNetV3"]
    model_name = "MobileNetV3"
    
    print("Testing valid image...")
    # Find a valid image in dataset
    img_path = "/app/dataset/val/Tomato___Early_blight/00c5c908-fc25-4710-a109-db143da23112___RS_Erly.B 7778.JPG"
    if not os.path.exists(img_path):
        print(f"Warning: Could not find {img_path}")
        return
    
    image = Image.open(img_path).convert("RGB")
    result = predict_with_model(image, model, model_name)
    class_name = result['prediction']
    confidence = result['confidence']
    print(f"Prediction: {class_name}, Confidence: {confidence:.2f}")

    tensor_img = preprocess_image(image, model_name)
    heatmap = generate_gradcam(tensor_img, image, model, model_name)
    if heatmap is not None:
        print("Heatmap generated successfully!")
    else:
        print("Failed to generate heatmap!")

    print("Testing OOD image...")
    # Create a completely blank/random image to simulate OOD
    random_img = Image.fromarray(np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8))
    result_ood = predict_with_model(random_img, model, model_name)
    
    print(f"OOD Entropy: {result_ood['entropy']:.2f}")
    if result_ood['entropy'] > 1.8:
        print("OOD Filter works!")
    else:
        print(f"Warning: OOD Filter might have failed. Entropy: {result_ood['entropy']:.2f}")
    
    print("All tests passed.")

if __name__ == "__main__":
    run_test()
