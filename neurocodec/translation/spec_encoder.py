from __future__ import annotations
import torch
from torch import nn
from .spec import spec_to_vector

class FormatSpecEncoder(nn.Module):
    def __init__(self,spec_dim=16,latent_dim=16):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(spec_dim,32),nn.GELU(),nn.Linear(32,latent_dim))
    def forward(self,spec_vector):
        return self.net(spec_vector)

    def encode_spec(self,spec):
        x=torch.tensor([spec_to_vector(spec)],dtype=torch.float32)
        with torch.inference_mode(): return self(x)[0]
