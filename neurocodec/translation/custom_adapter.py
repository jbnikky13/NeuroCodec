from __future__ import annotations
import torch
from torch import nn
from .custom_spec import validate_custom_spec
from .spec import spec_to_vector
from .spec_encoder import FormatSpecEncoder
from ..core.features import record_to_features
from ..models.parallel import ParallelEncoder
from ..training.spec_experiment import ConditionalDecoder

class CustomFormatAdapter:
    """Adapt the shared model to a previously unregistered format specification."""
    def __init__(self, data_encoder=None, spec_encoder=None, decoder=None, lr=5e-4):
        self.data_encoder=data_encoder or ParallelEncoder()
        self.spec_encoder=spec_encoder or FormatSpecEncoder()
        self.decoder=decoder or ConditionalDecoder()
        self.lr=lr

    def adapt(self, records:list[dict], spec:dict, steps:int=8)->list[float]:
        spec=validate_custom_spec(spec)
        if not records: raise ValueError("records cannot be empty")
        x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
        spec_x=torch.tensor([spec_to_vector(spec)],dtype=torch.float32)
        opt=torch.optim.AdamW(
            list(self.data_encoder.parameters())+
            list(self.spec_encoder.parameters())+
            list(self.decoder.parameters()),lr=self.lr)
        loss_fn=nn.MSELoss(); history=[]
        for _ in range(steps):
            opt.zero_grad()
            data_z=self.data_encoder(x)
            spec_z=self.spec_encoder(spec_x).expand(x.size(0),-1)
            pred=self.decoder(data_z,spec_z)
            loss=loss_fn(pred,x)
            loss.backward(); opt.step()
            history.append(float(loss.detach()))
        return history

    @torch.inference_mode()
    def encode(self,record:dict,spec:dict)->torch.Tensor:
        spec=validate_custom_spec(spec)
        x=torch.tensor([record_to_features(record)],dtype=torch.float32)
        s=torch.tensor([spec_to_vector(spec)],dtype=torch.float32)
        return self.decoder(self.data_encoder(x),self.spec_encoder(s))[0]
