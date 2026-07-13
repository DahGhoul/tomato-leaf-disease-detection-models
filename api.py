from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import numpy as np
import time
import joblib
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import base64

app = FastAPI(title="Tomato Leaf Disease API")

# Mapeo de clases
DISEASE_CLASSES = [
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]
NUM_CLASSES = len(DISEASE_CLASSES)

loaded_models = {}
loaded_hybrids = {}

# Transformaciones (mismo pipeline del frontend y entrenamiento)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.on_event("startup")
async def load_all_models():
    print("Cargando modelos en memoria...")
    
    try:
        # 1. MobileNetV3 (Clásico)
        m1 = models.mobilenet_v3_large(weights=None)
        m1.classifier[3] = nn.Linear(m1.classifier[3].in_features, NUM_CLASSES)
        m1.load_state_dict(torch.load("models/best_model.pth", map_location='cpu'))
        m1.eval()
        loaded_models["MobileNetV3"] = m1
        
        mob_ext = models.mobilenet_v3_large(weights=None)
        mob_ext.classifier[3] = nn.Linear(mob_ext.classifier[3].in_features, NUM_CLASSES)
        mob_ext.load_state_dict(torch.load("models/best_model.pth", map_location='cpu'))
        mob_ext.classifier = nn.Identity()
        mob_ext.eval()
        loaded_models["MobileNet_Extractor"] = mob_ext
    except Exception as e:
        print(f"Error cargando MobileNetV3: {e}")
        
    try:
        # 2. EfficientNetB7 (Clásico)
        m2 = models.efficientnet_b7(weights=None)
        m2.classifier = nn.Linear(m2.classifier[1].in_features, NUM_CLASSES)
        m2.load_state_dict(torch.load("models/plant_disease_model.pth", map_location='cpu'))
        m2.eval()
        loaded_models["EfficientNet"] = m2
        
        eff_ext = models.efficientnet_b7(weights=None)
        eff_ext.classifier = nn.Linear(eff_ext.classifier[1].in_features, NUM_CLASSES)
        eff_ext.load_state_dict(torch.load("models/plant_disease_model.pth", map_location='cpu'))
        eff_ext.classifier = nn.Identity()
        eff_ext.eval()
        loaded_models["EfficientNet_Extractor"] = eff_ext
    except Exception as e:
        print(f"Error cargando EfficientNet: {e}")

    # Híbridos
    try:
        loaded_hybrids["MobileNetV3_SVM"] = joblib.load("models/MobileNetV3_SVM.pkl")["model"]
    except Exception as e:
        print(f"Error cargando SVM: {e}")
        
    try:
        loaded_hybrids["EfficientNet_RF"] = joblib.load("models/EfficientNet_RF.pkl")["model"]
    except Exception as e:
        print(f"Error cargando RF: {e}")

    print("Modelos cargados exitosamente.")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor_img = transform(image).unsqueeze(0)
    
    results = {}
    
    # Modelos clásicos
    for model_name in ["MobileNetV3", "EfficientNet"]:
        if model_name not in loaded_models:
            continue
        model = loaded_models[model_name]
        start_time = time.time()
        with torch.no_grad():
            outputs = model(tensor_img)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            pred_idx = torch.argmax(probs).item()
        inf_time = time.time() - start_time
        
        probs_np = probs.cpu().numpy()
        disease = DISEASE_CLASSES[pred_idx]
        
        results[model_name] = {
            "prediction": disease,
            "confidence": float(probs_np[pred_idx]),
            "inference_time": inf_time,
            "probabilities": probs_np.tolist()
        }
        
    # Modelos híbridos
    if "MobileNetV3_SVM" in loaded_hybrids and "MobileNet_Extractor" in loaded_models:
        start_time = time.time()
        with torch.no_grad():
            feat = loaded_models["MobileNet_Extractor"](tensor_img).cpu().numpy().flatten().reshape(1, -1)
        svm_model = loaded_hybrids["MobileNetV3_SVM"]
        probs_np = svm_model.predict_proba(feat)[0]
        pred_idx = np.argmax(probs_np)
        inf_time = time.time() - start_time
        
        results["MobileNetV3_SVM"] = {
            "prediction": DISEASE_CLASSES[pred_idx],
            "confidence": float(probs_np[pred_idx]),
            "inference_time": inf_time,
            "probabilities": probs_np.tolist()
        }
        
    if "EfficientNet_RF" in loaded_hybrids and "EfficientNet_Extractor" in loaded_models:
        start_time = time.time()
        with torch.no_grad():
            feat = loaded_models["EfficientNet_Extractor"](tensor_img).cpu().numpy().flatten().reshape(1, -1)
        rf_model = loaded_hybrids["EfficientNet_RF"]
        probs_np = rf_model.predict_proba(feat)[0]
        pred_idx = np.argmax(probs_np)
        inf_time = time.time() - start_time
        
        results["EfficientNet_RF"] = {
            "prediction": DISEASE_CLASSES[pred_idx],
            "confidence": float(probs_np[pred_idx]),
            "inference_time": inf_time,
            "probabilities": probs_np.tolist()
        }
        
    return JSONResponse(content={"predictions": results})

@app.post("/gradcam")
async def get_gradcam(model_name: str, file: UploadFile = File(...)):
    if model_name not in loaded_models or "Extractor" in model_name:
        return {"error": "GradCAM no disponible para este modelo."}
        
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor_img = transform(image).unsqueeze(0)
    
    model = loaded_models[model_name]
    
    if "Efficient" in model_name:
        target_layers = [model.features[-1]]
    else: # MobileNet
        target_layers = [model.features[-1]]
        
    try:
        # Hacer prediccion real para obtener el target index de GradCAM
        with torch.no_grad():
            outputs = model(tensor_img)
            pred_idx = torch.argmax(outputs[0]).item()
            
        cam = GradCAM(model=model, target_layers=target_layers)
        targets = [ClassifierOutputTarget(pred_idx)]
        grayscale_cam = cam(input_tensor=tensor_img, targets=targets)[0, :]
        
        img_np = np.array(image.resize((224, 224))) / 255.0
        cam_image = show_cam_on_image(img_np, grayscale_cam, use_rgb=True)
        
        cam_pil = Image.fromarray(cam_image)
        buffered = io.BytesIO()
        cam_pil.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return JSONResponse(content={"gradcam_base64": img_str})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
