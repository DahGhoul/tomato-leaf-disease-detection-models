import re
import os

with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# 1. Imports
imports_to_add = '''import torch
import torch.nn as nn
from torchvision import models, transforms
import joblib
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import gc
'''
if 'import torch' not in app_code:
    app_code = app_code.replace('import streamlit as st\n', 'import streamlit as st\n' + imports_to_add)

# 2. Disease Classes & Transform
ml_constants = '''
# Mapeo de clases y Transformaciones
DISEASE_CLASSES = [
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]
NUM_CLASSES = len(DISEASE_CLASSES)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model_for_inference(model_name):
    \"\"\"Lazy loader para evitar OOM en Streamlit Cloud\"\"\"
    if model_name == "MobileNetV3":
        m = models.mobilenet_v3_large(weights=None)
        m.classifier[3] = nn.Linear(m.classifier[3].in_features, NUM_CLASSES)
        m.load_state_dict(torch.load("models/best_model.pth", map_location='cpu'))
        m.eval()
        return m
    elif model_name == "MobileNet_Extractor":
        m = models.mobilenet_v3_large(weights=None)
        m.classifier[3] = nn.Linear(m.classifier[3].in_features, NUM_CLASSES)
        m.load_state_dict(torch.load("models/best_model.pth", map_location='cpu'))
        m.classifier = nn.Identity()
        m.eval()
        return m
    elif model_name == "EfficientNet":
        m = models.efficientnet_b7(weights=None)
        m.classifier = nn.Linear(m.classifier[1].in_features, NUM_CLASSES)
        m.load_state_dict(torch.load("models/plant_disease_model.pth", map_location='cpu'))
        m.eval()
        return m
    elif model_name == "EfficientNet_Extractor":
        m = models.efficientnet_b7(weights=None)
        m.classifier = nn.Linear(m.classifier[1].in_features, NUM_CLASSES)
        m.load_state_dict(torch.load("models/plant_disease_model.pth", map_location='cpu'))
        m.classifier = nn.Identity()
        m.eval()
        return m
    elif model_name == "ResNet50":
        m = models.resnet50(weights=None)
        m.fc = nn.Linear(m.fc.in_features, NUM_CLASSES)
        # m.load_state_dict(torch.load("models/resnet_model.pth", map_location='cpu'))
        m.eval()
        return m
    elif model_name == "MobileNetV3_SVM":
        return joblib.load("models/MobileNetV3_SVM.pkl")["model"]
    elif model_name == "EfficientNet_RF":
        return joblib.load("models/EfficientNet_RF.pkl")["model"]
    return None

'''
if 'DISEASE_CLASSES =' not in app_code:
    # Insert after st.set_page_config
    app_code = re.sub(r'(st\.set_page_config\(.*?\)\n)', r'\1' + ml_constants, app_code, flags=re.DOTALL)

# 3. Replace call_predict_api
new_predict = '''def call_predict_api(image, fast_mode=False):
    if getattr(image, 'mode', '') != 'RGB':
        image = image.convert('RGB')
        
    tensor_img = transform(image).unsqueeze(0)
    results = {}
    import time
    
    # Determinar qué modelos correr
    if fast_mode:
        classic_models = ["MobileNetV3"]
        hybrid_models = ["MobileNetV3_SVM"]
    else:
        classic_models = ["MobileNetV3", "EfficientNet", "ResNet50"]
        hybrid_models = ["MobileNetV3_SVM", "EfficientNet_RF"]
        
    # Modelos clásicos
    for model_name in classic_models:
        try:
            model = load_model_for_inference(model_name)
            start_time = time.time()
            with torch.no_grad():
                outputs = model(tensor_img)
                probs = torch.nn.functional.softmax(outputs[0], dim=0)
                pred_idx = torch.argmax(probs).item()
            inf_time = time.time() - start_time
            probs_np = probs.cpu().numpy()
            results[model_name] = {
                "prediction": DISEASE_CLASSES[pred_idx],
                "confidence": float(probs_np[pred_idx]),
                "inference_time": inf_time,
                "probabilities": probs_np.tolist()
            }
            del model
            gc.collect()
        except Exception as e:
            st.warning(f"Error con {model_name}: {e}")
            
    # Modelos híbridos
    if "MobileNetV3_SVM" in hybrid_models:
        try:
            ext = load_model_for_inference("MobileNet_Extractor")
            svm_model = load_model_for_inference("MobileNetV3_SVM")
            start_time = time.time()
            with torch.no_grad():
                feat = ext(tensor_img).cpu().numpy().flatten().reshape(1, -1)
            probs_np = svm_model.predict_proba(feat)[0]
            pred_idx = np.argmax(probs_np)
            inf_time = time.time() - start_time
            results["MobileNetV3_SVM"] = {
                "prediction": DISEASE_CLASSES[pred_idx],
                "confidence": float(probs_np[pred_idx]),
                "inference_time": inf_time,
                "probabilities": probs_np.tolist()
            }
            del ext
            del svm_model
            gc.collect()
        except Exception as e:
            st.warning(f"Error con SVM: {e}")
            
    if "EfficientNet_RF" in hybrid_models:
        try:
            ext = load_model_for_inference("EfficientNet_Extractor")
            rf_model = load_model_for_inference("EfficientNet_RF")
            start_time = time.time()
            with torch.no_grad():
                feat = ext(tensor_img).cpu().numpy().flatten().reshape(1, -1)
            probs_np = rf_model.predict_proba(feat)[0]
            pred_idx = np.argmax(probs_np)
            inf_time = time.time() - start_time
            results["EfficientNet_RF"] = {
                "prediction": DISEASE_CLASSES[pred_idx],
                "confidence": float(probs_np[pred_idx]),
                "inference_time": inf_time,
                "probabilities": probs_np.tolist()
            }
            del ext
            del rf_model
            gc.collect()
        except Exception as e:
            st.warning(f"Error con RF: {e}")

    return results'''

app_code = re.sub(r'def call_predict_api\(image\):.*?return results\n', new_predict + '\n', app_code, flags=re.DOTALL)
app_code = app_code.replace('def call_predict_api(image):', new_predict) # in case regex failed

# 4. Replace call_gradcam_api
new_gradcam = '''def call_gradcam_api(image, model_name):
    if getattr(image, 'mode', '') != 'RGB':
        image = image.convert('RGB')
        
    if "Extractor" in model_name or model_name in ["MobileNetV3_SVM", "EfficientNet_RF"]:
        return None
        
    try:
        tensor_img = transform(image).unsqueeze(0)
        model = load_model_for_inference(model_name)
        
        if "Efficient" in model_name:
            target_layers = [model.features[-1]]
        elif "ResNet" in model_name:
            target_layers = [model.layer4[-1]]
        else: # MobileNet
            target_layers = [model.features[-1]]
            
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
        
        del model
        gc.collect()
        return img_str
    except Exception as e:
        print(f"GradCAM error: {e}")
        return None'''

app_code = re.sub(r'def call_gradcam_api\(image, model_name\):.*?return None\n', new_gradcam + '\n', app_code, flags=re.DOTALL)
app_code = app_code.replace('def call_gradcam_api(image, model_name):', new_gradcam) # in case regex failed

# 5. Fix UI Header and Add Radio Button
# Find the CSS block and replace main-header
css_replacement = '''
    .main-header {
        text-align: center;
        padding: 1rem;
        background: transparent;
        color: white;
        border-bottom: 1px solid #4a5568;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        font-size: 1.8rem;
        margin: 0;
        font-weight: 600;
        color: #e2e8f0;
    }
'''
app_code = re.sub(r'\.main-header \{.*?margin-bottom: 2rem;\n    \}', css_replacement, app_code, flags=re.DOTALL)

# Find st.sidebar
sidebar_addition = '''
        st.markdown("### ⚙️ Modo de Análisis")
        fast_mode = st.radio(
            "Selecciona la exhaustividad:",
            ("🚀 Rápido (MobileNet)", "🧠 Completo (5 Modelos)")
        ) == "🚀 Rápido (MobileNet)"
        st.markdown("---")
'''
if 'fast_mode = st.radio' not in app_code:
    app_code = app_code.replace('    with st.sidebar:\n        st.title("⚙️ Configuración")', '    with st.sidebar:\n        st.title("⚙️ Configuración")\n' + sidebar_addition)

# Update the call in main()
app_code = app_code.replace('preds = call_predict_api(image)', 'preds = call_predict_api(image, fast_mode)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)
