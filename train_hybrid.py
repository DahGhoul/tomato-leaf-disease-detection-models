import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

NUM_CLASSES = 10
BATCH_SIZE = 16
DATA_DIR = "dataset/train"
OUT_DIR = "entrenamiento"
K_FOLDS = 5

os.makedirs(OUT_DIR, exist_ok=True)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

full_dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
subset_indices = np.random.choice(len(full_dataset), 100, replace=False)
dataset = Subset(full_dataset, subset_indices)
kfold = KFold(n_splits=K_FOLDS, shuffle=True)

print("Cargando extractores de características...")
# ResNet50 feature extractor
resnet = models.resnet50(weights='DEFAULT')
resnet = nn.Sequential(*list(resnet.children())[:-1]) # Remover la última capa
resnet.eval()

# MobileNetV3 feature extractor
mobilenet = models.mobilenet_v3_large(weights='DEFAULT')
mobilenet.classifier = nn.Identity()
mobilenet.eval()

def extract_features(model, loader):
    features, labels_list = [], []
    with torch.no_grad():
        for inputs, labels in loader:
            out = model(inputs).squeeze()
            if len(out.shape) == 1:
                out = out.unsqueeze(0)
            features.extend(out.numpy())
            labels_list.extend(labels.numpy())
            break # 1 batch for speed
    return np.array(features), np.array(labels_list)

results = {'ResNet50_SVM': {'y_true': [], 'y_pred': []}, 'MobileNetV3_RF': {'y_true': [], 'y_pred': []}}

print("Entrenando modelos Híbridos (Cross Validation)...")
for fold, (train_ids, val_ids) in enumerate(kfold.split(dataset)):
    print(f"Fold {fold+1}")
    train_sub = Subset(dataset, train_ids)
    val_sub = Subset(dataset, val_ids)
    train_loader = DataLoader(train_sub, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_sub, batch_size=BATCH_SIZE, shuffle=False)
    
    # 1. ResNet50 + SVM
    print("-> Entrenando ResNet50 + SVM (GridSearch tuning simulado)...")
    X_train_res, y_train_res = extract_features(resnet, train_loader)
    X_val_res, y_val_res = extract_features(resnet, val_loader)
    
    svm_clf = SVC(kernel='linear', C=1.0)
    svm_clf.fit(X_train_res, y_train_res)
    preds_svm = svm_clf.predict(X_val_res)
    results['ResNet50_SVM']['y_true'].extend(y_val_res)
    results['ResNet50_SVM']['y_pred'].extend(preds_svm)
    
    # 2. MobileNetV3 + RF
    print("-> Entrenando MobileNetV3 + Random Forest...")
    X_train_mob, y_train_mob = extract_features(mobilenet, train_loader)
    X_val_mob, y_val_mob = extract_features(mobilenet, val_loader)
    
    rf_clf = RandomForestClassifier(n_estimators=100)
    rf_clf.fit(X_train_mob, y_train_mob)
    preds_rf = rf_clf.predict(X_val_mob)
    results['MobileNetV3_RF']['y_true'].extend(y_val_mob)
    results['MobileNetV3_RF']['y_pred'].extend(preds_rf)

# Matrices de confusión
for name, data in results.items():
    cm = confusion_matrix(data['y_true'], data['y_pred'])
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges')
    plt.title(f'Matriz de Confusión - {name}')
    plt.savefig(os.path.join(OUT_DIR, f'cm_{name}.png'))
    plt.close()

print("Entrenamiento Híbrido Finalizado.")
