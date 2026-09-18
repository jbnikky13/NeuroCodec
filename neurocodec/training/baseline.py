from __future__ import annotations
import torch
from torch import nn
from ..core.features import record_to_features
from ..data.generator import make_dataset
from ..models.parallel import ParallelEncoder

class LatentAutoencoder(nn.Module):
    def __init__(self,input_dim=16,latent_dim=16):
        super().__init__()
        self.encoder=ParallelEncoder(input_dim=input_dim,latent_dim=latent_dim)
        self.decoder=nn.Sequential(nn.Linear(latent_dim,32),nn.GELU(),nn.Linear(32,input_dim))
    def forward(self,x):
        z=self.encoder(x); return self.decoder(z),z

def train_autoencoder(epochs:int=50,seed:int=42):
    torch.manual_seed(seed)
    records=make_dataset(256,seed)
    x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    model=LatentAutoencoder(); opt=torch.optim.AdamW(model.parameters(),lr=2e-3); loss_fn=nn.MSELoss()
    history=[]
    for _ in range(epochs):
        opt.zero_grad(); pred,_=model(x); loss=loss_fn(pred,x); loss.backward(); opt.step(); history.append(float(loss))
    return model,history
