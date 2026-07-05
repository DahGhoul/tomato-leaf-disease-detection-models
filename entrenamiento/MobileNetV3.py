import os
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models, datasets
from torch.utils.data import DataLoader
from tqdm import tqdm
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
}

# Dataset directories (update path if needed)
data_dir = './dataset'

# Create datasets
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}

# Dataloaders
dataloaders = {x: DataLoader(image_datasets[x], batch_size=32,
                             shuffle=True, num_workers=2)
               for x in ['train', 'val']}

# Class names
class_names = image_datasets['train'].classes
num_classes = len(class_names)

# Visualize one image from each class
import matplotlib.pyplot as plt
import numpy as np

def imshow(inp, title=None):
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = np.clip((inp * std + mean), 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.axis('off')

# Show one image per class
shown = set()
plt.figure(figsize=(15, 10))
for i, (inputs, labels) in enumerate(dataloaders['train']):
    for j in range(inputs.size(0)):
        label = labels[j].item()
        if label not in shown:
            plt.subplot(3, 4, len(shown)+1)
            imshow(inputs[j].cpu(), title=class_names[label])
            shown.add(label)
        if len(shown) == num_classes:
            break
    if len(shown) == num_classes:
        break
plt.show()

# Load model
model = models.mobilenet_v3_large(weights='IMAGENET1K_V1')
model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)

# Send to device and enable multi-GPU if available
model = model.to(device)
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = nn.DataParallel(model)

# Loss, optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# Early stopping params
best_loss = float('inf')
best_model_wts = copy.deepcopy(model.state_dict())
early_stop_counter = 0
patience = 5

# Logs
train_loss_list, val_loss_list = [], []
train_acc_list, val_acc_list = [], []

# Training loop
num_epochs = 100

for epoch in range(num_epochs):
    print(f"\nEpoch {epoch+1}/{num_epochs}")

    for phase in ['train', 'val']:
        model.train() if phase == 'train' else model.eval()
        running_loss = 0.0
        running_corrects = 0

        dataloader = dataloaders[phase]
        phase_bar = tqdm(dataloader, desc=f"{phase.capitalize()} [{epoch+1}/{num_epochs}]", leave=False)

        for inputs, labels in phase_bar:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()

            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                if phase == 'train':
                    loss.backward()
                    optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

            phase_bar.set_postfix({
                "Loss": loss.item(),
                "Acc": (torch.sum(preds == labels.data).double() / inputs.size(0)).item()
            })

        epoch_loss = running_loss / len(image_datasets[phase])
        epoch_acc = running_corrects.double() / len(image_datasets[phase])

        if phase == 'train':
            train_loss_list.append(epoch_loss)
            train_acc_list.append(epoch_acc.item())
        else:
            val_loss_list.append(epoch_loss)
            val_acc_list.append(epoch_acc.item())
            if epoch_loss < best_loss:
                best_loss = epoch_loss
                best_model_wts = copy.deepcopy(model.state_dict())
                # --- aquí la corrección ---
                if isinstance(model, nn.DataParallel):
                    torch.save(model.module.state_dict(), 'best_model.pth')
                else:
                    torch.save(model.state_dict(), 'best_model.pth')
                # --------------------------
                early_stop_counter = 0
            else:
                early_stop_counter += 1

        print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} | Acc: {epoch_acc:.4f}")

    if early_stop_counter >= patience:
        print("Early stopping triggered.")
        break

# Load best model
model.load_state_dict(best_model_wts)

# Plot training history
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_loss_list, label='Train Loss')
plt.plot(val_loss_list, label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss over Epochs')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(train_acc_list, label='Train Acc')
plt.plot(val_acc_list, label='Val Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Accuracy over Epochs')
plt.legend()

plt.tight_layout()
plt.show()

# Inference: visualize predictions on val
model.eval()
inputs, labels = next(iter(dataloaders['val']))
inputs = inputs.to(device)
outputs = model(inputs)
_, preds = torch.max(outputs, 1)

plt.figure(figsize=(15, 8))
for i in range(8):
    ax = plt.subplot(2, 4, i + 1)
    imshow(inputs[i].cpu())
    ax.set_title(f"Pred: {class_names[preds[i]]}\nTrue: {class_names[labels[i]]}")
plt.tight_layout()
plt.show()