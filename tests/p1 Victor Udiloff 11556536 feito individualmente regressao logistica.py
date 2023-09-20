#p1 Vicor Udiloff 11556536 feio individualmente regressão logistica


import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import matplotlib.pyplot as plt

data_train = pd.read_csv(
    "https://media.githubusercontent.com/media/psi3471/datasets/main/disease_prediction/disease_train.csv"
).drop(columns=["Unnamed: 0"])

data_test = pd.read_csv(
    "https://media.githubusercontent.com/media/psi3471/datasets/main/disease_prediction/disease_test.csv"
).drop(columns=["Unnamed: 0"])

data_train = data_train.to_numpy()
data_test = data_test.to_numpy()
X1 = data_train[:,0:8]
Y1 = data_train[:,8]
X2 = data_test[:,0:8]
Y2 = data_test[:,8]

for i in range(X1.shape[1]):
    X1[:,i] = X1[:,i]/np.mean(X1[:,i])
    X2[:,i] = X2[:,i]/np.mean(X2[:,i])

X1 = torch.tensor(X1, dtype=torch.float32)
Y1 = torch.tensor(Y1, dtype=torch.float32).reshape(-1, 1)


X2 = torch.tensor(X2, dtype=torch.float32)
Y2 = torch.tensor(Y2, dtype=torch.float32).reshape(-1, 1)
print(Y2.shape)
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(8, 1)
        self.act1 = nn.Sigmoid()
    def forward(self, x):
        x = self.act1(self.hidden1(x))
        return x

model = Model()


loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

n_epochs = 3000
batch_size = 20

e = []

for epoch in range(n_epochs):
    for i in range(0, len(X1), batch_size):
        Xbatch = X1[i:i+batch_size]
        y_pred = model(Xbatch)
        ybatch = Y1[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    e.append(loss.item())
    if epoch % 400 == 0:
        print(f'Época: {epoch}, loss: {loss}')

plt.plot(e)

with torch.no_grad():
    y_pred = model(X2)
 


vp =0
vn=0
fp=0
fn=0

for i in range(150):
  if y_pred[i] > 0.5 and Y2[i]>0.5:
    vp +=1
  if y_pred[i] < 0.5 and Y2[i]>0.5:
    fn +=1
  if y_pred[i] < 0.5 and Y2[i]<0.5:
    vn +=1
  if y_pred[i] > 0.5 and Y2[i]<0.5:
    fp +=1

precisao = (vp)/(vp+fp)
sensibilidade = (vp)/(vp+fn)

f1score = 2*(precisao*sensibilidade)/(precisao+sensibilidade)

print("Acurácia=", 100*((vp+vn)/(vp+vn+fp+fn)),"%")
print("Matriz de confusão:",[[vp,fp],[fn,vn]])
print("F1-Score", f1score)