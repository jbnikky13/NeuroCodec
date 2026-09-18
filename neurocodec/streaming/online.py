from __future__ import annotations
import torch
from torch import nn
from ..core.features import record_to_features
from ..models.parallel import ParallelEncoder
from ..translation.spec import format_spec,spec_to_vector
from ..translation.spec_encoder import FormatSpecEncoder
from ..training.spec_experiment import ConditionalDecoder

class OnlineAdapter:
    """Small online adaptation loop for recent observations.

    The adapter updates a copy of the learned components using a bounded
    stream window. It is deliberately conservative: callers control steps
    and learning rate, and the original models remain untouched.
    """
    def __init__(self,data_encoder=None,spec_encoder=None,decoder=None,lr=5e-4):
        self.data_encoder=data_encoder or ParallelEncoder()
        self.spec_encoder=spec_encoder or FormatSpecEncoder()
        self.decoder=decoder or ConditionalDecoder()
        self.lr=lr

    def adapt(self,records:list[dict],target_format:str,steps:int=3)->list[float]:
        if not records: raise ValueError("records cannot be empty")
        if steps < 1: raise ValueError("steps must be positive")
        x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
        spec=torch.tensor([spec_to_vector(format_spec(target_format))],dtype=torch.float32)
        params=list(self.data_encoder.parameters())+list(self.spec_encoder.parameters())+list(self.decoder.parameters())
        optimizer=torch.optim.AdamW(params,lr=self.lr)
        loss_fn=nn.MSELoss(); history=[]
        for _ in range(steps):
            optimizer.zero_grad()
            data_z=self.data_encoder(x)
            spec_z=self.spec_encoder(spec).expand(x.size(0),-1)
            pred=self.decoder(data_z,spec_z)
            loss=loss_fn(pred,x)
            loss.backward(); optimizer.step()
            history.append(float(loss.detach()))
        return history

    @torch.inference_mode()
    def predict(self,record:dict,target_format:str)->torch.Tensor:
        x=torch.tensor([record_to_features(record)],dtype=torch.float32)
        spec=torch.tensor([spec_to_vector(format_spec(target_format))],dtype=torch.float32)
        z=self.data_encoder(x)
        s=self.spec_encoder(spec)
        return self.decoder(z,s)[0]
