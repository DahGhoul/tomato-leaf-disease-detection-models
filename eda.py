import os
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from collections import Counter

DATASET_PATH = "dataset/train"
EDA_OUT_DIR = "temp/eda"

def run_eda():
    os.makedirs(EDA_OUT_DIR, exist_ok=True)
    
    classes = [d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]
    
    class_counts = {}
    for cls in classes:
        cls_path = os.path.join(DATASET_PATH, cls)
        count = len(glob.glob(os.path.join(cls_path, "*.JPG"))) + len(glob.glob(os.path.join(cls_path, "*.png"))) + len(glob.glob(os.path.join(cls_path, "*.jpg")))
        class_counts[cls] = count
        
        # Guardar conteos en JSON
    
    # Extraer estadísticos de una muestra
    print("Calculando estadísticos descriptivos...")
    sample_size = min(1000, sum(class_counts.values()))
    all_images = glob.glob(os.path.join(DATASET_PATH, "*", "*.jpg")) + glob.glob(os.path.join(DATASET_PATH, "*", "*.png"))
    np.random.shuffle(all_images)
    sample = all_images[:sample_size]
    
    widths, heights = [], []
    r_means, g_means, b_means = [], [], []
    
    for img_path in sample:
        try:
            img = Image.open(img_path).convert('RGB')
            w, h = img.size
            widths.append(w)
            heights.append(h)
            
            img_arr = np.array(img)
            r_means.append(np.mean(img_arr[:,:,0]))
            g_means.append(np.mean(img_arr[:,:,1]))
            b_means.append(np.mean(img_arr[:,:,2]))
        except Exception:
            continue
            
    stats = {
        "class_counts": class_counts,
        "descriptive": {
            "total_images": sum(class_counts.values()),
            "avg_width": float(np.mean(widths)),
            "avg_height": float(np.mean(heights)),
            "avg_r": float(np.mean(r_means)),
            "avg_g": float(np.mean(g_means)),
            "avg_b": float(np.mean(b_means))
        }
    }
    
    with open(os.path.join(EDA_OUT_DIR, "eda_stats.json"), "w") as f:
        json.dump(stats, f)
        
    # Graficar distribución
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(class_counts.values()), y=list(class_counts.keys()), palette="viridis", hue=list(class_counts.keys()), legend=False)
    plt.title("Distribución de Imágenes por Clase (Dataset de Entrenamiento)")
    plt.xlabel("Cantidad de Imágenes")
    plt.ylabel("Enfermedad")
    plt.tight_layout()
    plt.savefig(os.path.join(EDA_OUT_DIR, "class_distribution.png"))
    plt.close()
    
    print("EDA finalizado exitosamente. Gráficos guardados en temp/eda/")

if __name__ == "__main__":
    run_eda()
