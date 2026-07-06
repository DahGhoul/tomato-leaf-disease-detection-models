import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Imports
imports = '''import warnings
import cv2
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
from streamlit_image_comparison import image_comparison
'''
content = content.replace("import warnings\n", imports)

# 2. Add TREATMENT_INFO
treatment_info = '''
TREATMENT_INFO = {
    'Bacterial_spot': {'water': 'Riego por goteo estricto', 'chem': 'Fungicidas con Cobre', 'prev': 'Desinfectar herramientas'},
    'Early_blight': {'water': 'Evitar mojar hojas', 'chem': 'Mancozeb o Clorotalonil', 'prev': 'Rotación de cultivos'},
    'Late_blight': {'water': 'Mantener follaje seco', 'chem': 'Metalaxil u Oxatiapiprolina', 'prev': 'Destruir plantas infectadas'},
    'Leaf_Mold': {'water': 'Mejorar ventilación', 'chem': 'Fungicidas a base de cobre', 'prev': 'Reducir humedad en invernadero'},
    'Septoria_leaf_spot': {'water': 'Riego en la base', 'chem': 'Clorotalonil', 'prev': 'Eliminar malezas'},
    'Spider_mites': {'water': 'Riego abundante', 'chem': 'Acaricidas (Abamectina)', 'prev': 'Control biológico'},
    'Target_Spot': {'water': 'Evitar riego nocturno', 'chem': 'Fungicidas sistémicos', 'prev': 'Poda de hojas inferiores'},
    'Tomato_Yellow_Leaf_Curl_Virus': {'water': 'Riego normal', 'chem': 'Insecticidas para Mosca Blanca', 'prev': 'Mallas anti-insectos'},
    'Tomato_mosaic_virus': {'water': 'Riego normal', 'chem': 'Ninguno (Virus)', 'prev': 'Lavar manos, semillas certificadas'},
    'healthy': {'water': 'Riego normal y balanceado', 'chem': 'Ninguno', 'prev': 'Mantener buenas prácticas agrícolas'}
}
'''
content = content.replace("DISEASE_CLASSES = list(DISEASE_INFO.keys())", "DISEASE_CLASSES = list(DISEASE_INFO.keys())\n" + treatment_info)

# 3. Add Grad-CAM function
gradcam_func = '''
def generate_gradcam(image_tensor, original_image, model, model_name):
    try:
        if model_name == 'MobileNetV3':
            target_layers = [model.features[-1]]
        elif model_name == 'EfficientNetB7':
            target_layers = [model.features[-1]]
        else:
            return None
        
        cam = GradCAM(model=model, target_layers=target_layers)
        targets = [ClassifierOutputTarget(torch.argmax(model(image_tensor)).item())]
        grayscale_cam = cam(input_tensor=image_tensor, targets=targets)[0, :]
        
        # Resize original image to match tensor size
        size = (224, 224) if model_name != 'EfficientNetB7' else (128, 128)
        orig_img_resized = original_image.resize(size)
        rgb_img = np.float32(orig_img_resized) / 255
        
        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        return Image.fromarray(cam_image)
    except Exception as e:
        return None

def predict_with_model'''
content = content.replace("def predict_with_model", gradcam_func)

# 4. Update prediction entropy
old_pred_return = '''    return {
        'prediction': DISEASE_CLASSES[prediction],
        'probabilities': probabilities,
        'confidence': float(probabilities[prediction]),
        'inference_time': inference_time
    }'''
new_pred_return = '''    entropy = stats.entropy(probabilities)
    return {
        'prediction': DISEASE_CLASSES[prediction],
        'probabilities': probabilities,
        'confidence': float(probabilities[prediction]),
        'inference_time': inference_time,
        'entropy': entropy
    }'''
content = content.replace(old_pred_return, new_pred_return)

# 5. UI Updates
old_analysis = '''                # Botón de análisis
                if st.button("🔬 Analizar Imagen", type="primary"):
                    with st.spinner("Procesando..."):
                        st.session_state['predictions'] = {}
                        for model_name, model in models.items():
                            result = predict_with_model(image, model, model_name)
                            st.session_state['predictions'][model_name] = result'''

new_analysis = '''                # Botón de análisis
                if st.button("🔬 Analizar Imagen y Generar Grad-CAM", type="primary"):
                    with st.spinner("Ejecutando Inteligencia Artificial (Analizando patrones)..."):
                        # OOD Detection
                        dummy_res = predict_with_model(image, models['MobileNetV3'], 'MobileNetV3')
                        if dummy_res['entropy'] > 1.8:
                            st.error("🚨 ¡Alerta Anti-Engaños! La red neuronal tiene demasiada incertidumbre (Entropía alta). Por favor, asegúrate de subir una imagen clara de una hoja de tomate y no de otro objeto.")
                        else:
                            st.session_state['predictions'] = {}
                            st.session_state['gradcams'] = {}
                            for model_name, model in models.items():
                                result = predict_with_model(image, model, model_name)
                                st.session_state['predictions'][model_name] = result
                                
                                if model_name in ['MobileNetV3', 'EfficientNetB7']:
                                    tensor_img = preprocess_image(image, model_name)
                                    cam = generate_gradcam(tensor_img, image, model, model_name)
                                    st.session_state['gradcams'][model_name] = cam'''
content = content.replace(old_analysis, new_analysis)

# 6. Treatment Cards and Slider in UI
old_card = '''                        </div>
                    </div>
                    """, unsafe_allow_html=True)'''
                    
new_card = '''                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if disease in TREATMENT_INFO:
                        treat = TREATMENT_INFO[disease]
                        st.markdown(f"""
                        <div style="background: rgba(46, 204, 113, 0.15); padding: 1.5rem; border-radius: 10px; margin-top: 10px; border-left: 5px solid #2ecc71; margin-bottom: 20px;">
                            <h4 style="color: #2ecc71; margin-top: 0;">📋 Plan de Acción (Recomendación)</h4>
                            <p style="margin-bottom: 5px;">💧 <b>Riego:</b> {treat['water']}</p>
                            <p style="margin-bottom: 5px;">🧪 <b>Tratamiento:</b> {treat['chem']}</p>
                            <p style="margin-bottom: 0;">🛡️ <b>Prevención:</b> {treat['prev']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    if 'gradcams' in st.session_state and model_name in st.session_state['gradcams'] and st.session_state['gradcams'][model_name]:
                        st.markdown("#### 🔍 Análisis de Calor (Grad-CAM)")
                        st.markdown("<p style='font-size: 0.9rem; color: #aaa;'>Mueve el deslizador para ver exactamente qué partes de la hoja utilizó la IA para tomar su decisión.</p>", unsafe_allow_html=True)
                        cam_img = st.session_state['gradcams'][model_name]
                        orig_resized = image.resize(cam_img.size)
                        image_comparison(
                            img1=orig_resized,
                            img2=cam_img,
                            label1="Original",
                            label2="Atención IA",
                            width=500
                        )'''
content = content.replace(old_card, new_card)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
