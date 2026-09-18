from __future__ import annotations
import json
from typing import Any
from ..codecs.registry import get_codec

def record_to_target_vector(record:dict[str,Any], format_name:str)->list[float]:
    """Stable numeric target derived from the encoded representation.

    This is a format fingerprint for the held-out experiment, not a claim
    that bytes themselves are semantically understood by the network.
    """
    payload=get_codec(format_name).encode(record)
    raw=payload.encode()
    buckets=[0.0]*16
    for i,b in enumerate(raw):
        buckets[i%16]+=b/255.0
    scale=max(1,len(raw))
    return [min(1.0,v/scale*16.0) for v in buckets]

def target_matrix(records,format_name):
    import torch
    return torch.tensor([record_to_target_vector(r,format_name) for r in records],dtype=torch.float32)
