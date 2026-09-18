from __future__ import annotations
import torch
from torch import nn
from ..data.generator import make_dataset
from ..core.features import record_to_features
from ..models.parallel import ParallelEncoder
from ..translation.learned import FormatDecoder
from ..translation.targets import target_matrix

def train_heldout_experiment(held_out="pipe",epochs=100,seed=42):
    formats=["json","csv","pipe"]
    if held_out not in formats: raise ValueError("held_out must be json, csv or pipe")
    torch.manual_seed(seed)
    records=make_dataset(512,seed)
    x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    train_formats=[f for f in formats if f!=held_out]
    targets={f:target_matrix(records,f) for f in formats}
    encoder=ParallelEncoder()
    decoders=nn.ModuleDict({f:FormatDecoder() for f in train_formats})
    opt=torch.optim.AdamW(list(encoder.parameters())+list(decoders.parameters()),lr=2e-3)
    loss_fn=nn.MSELoss(); history=[]
    for _ in range(epochs):
        opt.zero_grad(); z=encoder(x)
        loss=sum(loss_fn(decoders[f](z),targets[f]) for f in train_formats)/len(train_formats)
        loss.backward(); opt.step(); history.append(float(loss))
    with torch.inference_mode():
        z=encoder(x)
        heldout_reference=targets[held_out]
        # Zero-shot proxy: nearest trained target head is intentionally not
        # treated as a decoder for the unseen format.
        train_errors={f:float(loss_fn(decoders[f](z),targets[f])) for f in train_formats}
    return {"encoder":encoder,"decoders":decoders,"history":history,"held_out":held_out,"heldout_target":heldout_reference,"train_errors":train_errors}
