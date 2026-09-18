from __future__ import annotations
import torch
from torch import nn
from ..models.parallel import ParallelEncoder

class FormatDecoder(nn.Module):
    def __init__(self,latent_dim=16,output_dim=16):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(latent_dim,32),nn.GELU(),nn.Linear(32,output_dim))
    def forward(self,z): return self.net(z)

class LearnedTranslator(nn.Module):
    def __init__(self,input_dim=16,latent_dim=16):
        super().__init__()
        self.encoder=ParallelEncoder(input_dim=input_dim,latent_dim=latent_dim)
        self.decoders=nn.ModuleDict()
    def add_decoder(self,name,output_dim=16):
        self.decoders[name]=FormatDecoder(16,output_dim)
    def encode(self,x): return self.encoder(x)
    def decode(self,z,target): return self.decoders[target](z)
