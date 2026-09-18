from __future__ import annotations
import torch
from torch import nn
from ..data.generator import make_dataset
from ..core.features import record_to_features
from ..translation.spec import format_spec
from ..translation.spec_encoder import FormatSpecEncoder

class ConditionalDecoder(nn.Module):
    def __init__(self,data_dim=16,latent_dim=16):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(data_dim+latent_dim,64),nn.GELU(),nn.Linear(64,16))
    def forward(self,data_latent,spec_latent):
        return self.net(torch.cat([data_latent,spec_latent],dim=-1))

def train_spec_conditioned(epochs=100,seed=42):
    torch.manual_seed(seed)
    records=make_dataset(384,seed)
    x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    from ..models.parallel import ParallelEncoder
    data_encoder=ParallelEncoder()
    spec_encoder=FormatSpecEncoder()
    decoder=ConditionalDecoder()
    formats=("json","csv","pipe")
    specs={f:spec_encoder(torch.tensor([__import__("neurocodec.translation.spec",fromlist=["spec_to_vector"]).spec_to_vector(format_spec(f))],dtype=torch.float32)) for f in formats}
    opt=torch.optim.AdamW(list(data_encoder.parameters())+list(spec_encoder.parameters())+list(decoder.parameters()),lr=2e-3)
    loss_fn=nn.MSELoss(); history=[]
    for _ in range(epochs):
        opt.zero_grad(); data_z=data_encoder(x); loss=0
        for f in formats:
            s=specs[f].expand(x.size(0),-1); pred=decoder(data_z,s); loss=loss+loss_fn(pred,x)
        loss=loss/len(formats); loss.backward(); opt.step(); history.append(float(loss))
    return {"data_encoder":data_encoder,"spec_encoder":spec_encoder,"decoder":decoder,"history":history,"formats":formats}
