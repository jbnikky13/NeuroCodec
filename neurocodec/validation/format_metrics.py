from __future__ import annotations
import torch

def vector_metrics(target:torch.Tensor,pred:torch.Tensor)->dict[str,float]:
    target,pred=target.float(),pred.float()
    mse=torch.mean((target-pred)**2).item()
    mae=torch.mean(torch.abs(target-pred)).item()
    return {"mse":mse,"mae":mae,"rmse":mse**0.5}

def cosine_similarity(target:torch.Tensor,pred:torch.Tensor)->float:
    return float(torch.nn.functional.cosine_similarity(target.float(),pred.float(),dim=-1).mean().item())
