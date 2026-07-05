"""
Entrenamiento de un clasificador SVM para el dataset `tomato`
=============================================================

Flujo:
1.  Extraer *embeddings* por imagen con un ResNet-50 pre-entrenado (feature-extractor, sin ajuste).
2.  Entrenar un SVM (RBF) sobre esos vectores.
3.  Evaluar y guardar el modelo.

Requisitos:
torch, torchvision, scikit-learn, numpy, joblib, tqdm
"""

import os
import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
from tqdm import tqdm


# ---------- 1. Configuración general ----------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
data_dir = './dataset'                       # .../train  y  .../val

# ---------- 2. Transformaciones (sin augment) ----------
tfm = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ---------- 3. Datasets y loaders ----------
sets = {split: datasets.ImageFolder(os.path.join(data_dir, split), tfm)
        for split in ['train', 'val']}

loaders = {split: DataLoader(sets[split], batch_size=64,
                             shuffle=False, num_workers=2)
           for split in ['train', 'val']}

class_names = sets['train'].classes
print(f"Número de clases: {len(class_names)} → {class_names}")

# ---------- 4. Feature extractor (congelado) ----------
feat_net = models.resnet50(weights='IMAGENET1K_V2')
feat_net.fc = torch.nn.Identity()          # quitamos la FC final
feat_net.eval().to(device)
for p in feat_net.parameters():
    p.requires_grad = False               # ¡totalmente congelado!

@torch.inference_mode()
def extract(loader):
    feats, labels = [], []
    for X, y in tqdm(loader, desc='Extrayendo'):
        X = X.to(device)
        feats.append(feat_net(X).cpu().numpy())
        labels.append(y.numpy())
    return np.concatenate(feats), np.concatenate(labels)

print("Extrayendo embeddings...")
X_train, y_train = extract(loaders['train'])
X_val,   y_val   = extract(loaders['val'])
print(f"Shape embeddings: {X_train.shape}")   # (N, 2048)

# ---------- 5. Entrenamiento SVM ----------
print("\nEntrenando SVM (kernel RBF)…")
svm = SVC(kernel='rbf', C=10, gamma='scale', probability=True)
svm.fit(X_train, y_train)

# ---------- 6. Evaluación ----------
val_pred = svm.predict(X_val)
acc = accuracy_score(y_val, val_pred)
print(f"\nAccuracy validación: {acc:.4f}\n")
print(classification_report(y_val, val_pred, target_names=class_names))

# ---------- 7. Guardar modelo ----------
joblib.dump({'svm': svm,
             'classes': class_names},
            'svm_tomato.pkl')
print("Modelo guardado en 'svm_tomato.pkl'")

