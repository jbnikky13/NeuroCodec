from __future__ import annotations
import torch
from torch import nn
from ..data.generator import make_dataset
from ..core.features import record_to_features
from ..translation.learned import LearnedTranslator

def train_format_experiment(epochs=80,seed=42):
    torch.manual_seed(seed)
    records=make_dataset(384,seed)
    x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    model=LearnedTranslator()
    for fmt in ("json","csv","pipe"): model.add_decoder(fmt)
    opt=torch.optim.AdamW(model.parameters(),lr=2e-3)
    loss_fn=nn.MSELoss()
    history=[]
    for _ in range(epochs):
        opt.zero_grad()
        z=model.encode(x)
        # In Phase 2 all known format views share the same canonical feature target.
        loss=sum(loss_fn(model.decode(z,fmt),x) for fmt in ("json","csv","pipe"))/3
        loss.backward(); opt.step(); history.append(float(loss))
    return model,history
