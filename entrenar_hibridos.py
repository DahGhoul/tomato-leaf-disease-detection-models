import os
import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

# Definir clases y rutas
dataset_dir = "dataset/val"
classes = sorted(os.listdir(dataset_dir))
NUM_CLASSES = len(classes)

# Transformaciones (las mismas de la API)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print("Cargando extractores de características clásicos...")
# 1. MobileNetV3 (Clásico)
mobilenet = models.mobilenet_v3_large(weights=None)
mobilenet.classifier[3] = nn.Linear(mobilenet.classifier[3].in_features, NUM_CLASSES)
mobilenet.load_state_dict(torch.load("models/best_model.pth", map_location='cpu'))
# Convertir a extractor
mobilenet.classifier = nn.Identity()
mobilenet.eval()

# 2. EfficientNetB7 (Clásico)
efficientnet = models.efficientnet_b7(weights=None)
efficientnet.classifier = nn.Linear(efficientnet.classifier[1].in_features, NUM_CLASSES)
efficientnet.load_state_dict(torch.load("models/plant_disease_model.pth", map_location='cpu'))
# Convertir a extractor (EfficientNetB0 output is 1280 dim before classifier)
efficientnet.classifier = nn.Identity()
efficientnet.eval()

print("Extrayendo características del dataset (1000 imágenes max)...")
X_mob = []
X_eff = []
y = []

# Iterar sobre las imágenes para extraer features
for i, cls_name in enumerate(classes):
    cls_dir = os.path.join(dataset_dir, cls_name)
    if not os.path.isdir(cls_dir): continue
    
    # Tomar hasta 50 imágenes por clase para rapidez (500 total)
    images = os.listdir(cls_dir)[:50]
    for img_name in images:
        img_path = os.path.join(cls_dir, img_name)
        try:
            image = Image.open(img_path).convert('RGB')
            tensor_img = transform(image).unsqueeze(0)
            
            with torch.no_grad():
                feat_mob = mobilenet(tensor_img).numpy().flatten()
                feat_eff = efficientnet(tensor_img).numpy().flatten()
            
            X_mob.append(feat_mob)
            X_eff.append(feat_eff)
            y.append(i)
        except Exception as e:
            print(f"Error procesando {img_path}: {e}")

X_mob = np.array(X_mob)
X_eff = np.array(X_eff)
y = np.array(y)

print(f"Características extraídas. Dim MobileNet: {X_mob.shape}, Dim EfficientNet: {X_eff.shape}")

print("Entrenando MobileNetV3 + SVM...")
svm_model = SVC(kernel='linear', probability=True, random_state=42)
svm_model.fit(X_mob, y)
joblib.dump({"model": svm_model, "classes": classes}, "models/MobileNetV3_SVM.pkl")

print("Entrenando EfficientNet + Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_eff, y)
joblib.dump({"model": rf_model, "classes": classes}, "models/EfficientNet_RF.pkl")

print("Entrenamiento completado exitosamente y modelos guardados en /models.")
