from __future__ import annotations
from typing import Any
import torch
from ..core.features import record_to_features
from .format_metrics import vector_metrics

def custom_format_metrics(adapter,records:list[dict[str,Any]],spec:dict[str,Any])->dict[str,float]:
    target=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    pred=torch.stack([adapter.encode(r,spec) for r in records])
    return vector_metrics(target,pred)
