import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, TensorDataset
import os

def run_training_loop(epochs, lr, batch_size, model_name, progress_callback, metric_callback):
    """
    Ejecuta un bucle de entrenamiento real en PyTorch.
    Usa el dataset real si existe, sino genera un dataset sintético para demostración.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 1. Preparar Modelo Base
    if model_name == "MobileNetV3":
        model = models.mobilenet_v3_small(pretrained=True)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, 10)
    elif model_name == "ResNet50":
        model = models.resnet50(pretrained=True)
        model.fc = nn.Linear(model.fc.in_features, 10)
    else: # EfficientNet
        model = models.efficientnet_b0(pretrained=True)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 10)
        
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # 2. Preparar Datos (Real o Sintético)
    data_dir = "dataset/train"
    if os.path.exists(data_dir) and len(os.listdir(data_dir)) > 0:
        # Usar datos reales
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        dataset = datasets.ImageFolder(data_dir, transform=transform)
        # Tomar un subset si es muy grande para no bloquear la web
        if len(dataset) > 1000:
            indices = torch.randperm(len(dataset))[:1000]
            dataset = torch.utils.data.Subset(dataset, indices)
    else:
        # Dataset Sintético para demostración visual
        X = torch.randn(100, 3, 224, 224)
        y = torch.randint(0, 10, (100,))
        dataset = TensorDataset(X, y)
        
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # 3. Bucle de Entrenamiento
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        # Calcular progreso por lotes
        total_batches = len(loader)
        
        for i, (inputs, labels) in enumerate(loader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Simular tiempo si el dataset es muy pequeño para que se aprecie la UI
            if len(dataset) <= 100:
                time.sleep(0.1)
                
            # Actualizar progreso global
            current_progress = (epoch * total_batches + i + 1) / (epochs * total_batches)
            progress_callback(current_progress)
            
        epoch_loss = running_loss / total_batches
        epoch_acc = correct / total
        
        # Callback para métricas
        metric_callback(epoch + 1, epoch_loss, epoch_acc)
        
    # 4. Guardar Modelo
    os.makedirs("models", exist_ok=True)
    save_path = f"models/{model_name}_custom.pt"
    torch.save(model.state_dict(), save_path)
    
    return save_path
