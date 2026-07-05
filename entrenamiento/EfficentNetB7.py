import torch 
from torch import nn
from torch.optim import Adam
from torchvision.transforms import transforms
from torch.utils.data import DataLoader, Dataset
from torchvision import models
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

train_data = './dataset/train'
val_data = './dataset/val'

filepaths = []
labels =[]

folds = os.listdir(train_data)
print(folds)
for fold in folds:
    fold_path = os.path.join(train_data, fold)

    for path in os.listdir(fold_path):
        filepath = os.path.join(fold_path, path)
        filepaths.append(filepath)
        labels.append(fold)

file_series=pd.Series(filepaths,name='filepaths')
label_series=pd.Series(labels,name='labels')
train_df=pd.concat([file_series,label_series],axis=1)

#test_data= test_data
filepaths=[]
labels=[]

folds=os.listdir(val_data)

for fold in folds:
    foldpath=os.path.join(val_data,fold)
    filelist=os.listdir(foldpath)

    for fpath in filelist:
        fillpath=os.path.join(foldpath,fpath)

        labels.append(fold)
        filepaths.append(fillpath)

file_series=pd.Series(filepaths,name='filepaths')
label_series=pd.Series(labels,name='labels')
ts_df=pd.concat([file_series,label_series],axis=1)

ts_df.shape

# spliting testing data
val_df, test_df = train_test_split(ts_df,test_size=0.5,random_state= 42)

print(train_df.shape)
print(val_df.shape)
print(test_df.shape)

label_encoder = LabelEncoder()
label_encoder.fit(train_df["labels"])

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.ConvertImageDtype(torch.float)
])

class CustomImageDataset(Dataset):
    def __init__(self,dataframe,transform=None):
        self.dataframe = dataframe
        self.transform = transform
        self.labels = torch.tensor(label_encoder.transform(dataframe['labels'])).to(device)

    def __len__(self):
        return self.dataframe.shape[0]

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx, 0]
        label = self.labels[idx]

        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = (self.transform(image)/255.0).to(device)

        return image, label

train_dataset = CustomImageDataset(dataframe = train_df, transform = transform)
val_dataset = CustomImageDataset(dataframe = val_df, transform = transform)
test_dataset = CustomImageDataset(dataframe = test_df, transform = transform)

train_dataset.__getitem__(2)

label_encoder.inverse_transform([2])

n_rows = 3
n_cols =3

f, axarr = plt.subplots(n_rows, n_cols)

for row in range(n_rows):
    for col in range(n_cols):
        image = Image.open(train_df.sample(n =1)["filepaths"].iloc[0]).convert('RGB')
        axarr[row,col].imshow(image)
        axarr[row,col].axis('off')

plt.tight_layout()
plt.show()        

LR = 1e-3
BATCH_SIZE = 4
EPOCHS =15

train_loader = DataLoader(train_dataset, batch_size = BATCH_SIZE, shuffle =True)
val_loader = DataLoader(val_dataset, batch_size = BATCH_SIZE, shuffle =True)
test_loader = DataLoader(test_dataset, batch_size = BATCH_SIZE, shuffle =True)

efficientnt_model = models.efficientnet_b7(weights = 'DEFAULT')

for param in efficientnt_model.parameters():
    param.requires_grad = True

efficientnt_model.classifier

num_classes = len(train_df['labels'].unique())
print(num_classes)

efficientnt_model.classifier = torch.nn.Linear(2560, 10)
efficientnt_model.classifier

efficientnt_model.to(device)

criterion =nn.CrossEntropyLoss()
optimizer =Adam(efficientnt_model.parameters(), lr =LR)


total_loss_train_plot = []
total_acc_train_plot=[]

for epoch in range(EPOCHS):
    total_acc_train =0
    total_loss_train =0


    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = efficientnt_model(inputs)
        train_loss = criterion(outputs, labels)
        total_loss_train += train_loss.item()

        train_loss.backward()
        train_acc = (torch.argmax(outputs, axis =1)==labels).sum().item()
        total_acc_train += train_acc

        optimizer.step()

    total_loss_train_plot.append(round(total_loss_train/1000, 4))
    total_acc_train_plot.append(round(total_acc_train/train_dataset.__len__()*100,4))

    print(f"Epoch {epoch+1}/{EPOCHS}, Train Loss: {round(total_loss_train/1000, 4)}, Train Accuracy: {round(total_acc_train/train_dataset.__len__()*100,4)} %")

with torch.no_grad():
    total_acc_test = 0

    for input, labels in test_loader:
        prediction = efficientnt_model(input)
        acc = (torch.argmax(prediction, axis =1) == labels).sum().item()
        total_acc_test += acc

print(round(total_acc_test/test_dataset.__len__()*100,2))

# Assuming 'model' is your trained PyTorch model
torch.save(efficientnt_model.state_dict(), "plant_disease_model.pth")