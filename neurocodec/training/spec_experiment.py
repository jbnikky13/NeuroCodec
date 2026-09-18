from __future__ import annotations

import torch
from torch import nn

from ..core.features import record_to_features
from ..data.generator import make_dataset
from ..models.parallel import ParallelEncoder
from ..translation.spec import format_spec, spec_to_vector
from ..translation.spec_encoder import FormatSpecEncoder


class ConditionalDecoder(nn.Module):
    def __init__(self, data_dim: int = 16, latent_dim: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(data_dim + latent_dim, 64),
            nn.GELU(),
            nn.Linear(64, 16),
        )

    def forward(self, data_latent: torch.Tensor, spec_latent: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat([data_latent, spec_latent], dim=-1))


def train_spec_conditioned(epochs: int = 100, seed: int = 42):
    torch.manual_seed(seed)
    records = make_dataset(384, seed)
    x = torch.tensor(
        [record_to_features(record) for record in records],
        dtype=torch.float32,
    )

    data_encoder = ParallelEncoder()
    spec_encoder = FormatSpecEncoder()
    decoder = ConditionalDecoder()
    formats = ("json", "csv", "pipe")

    # Keep raw specification vectors outside the autograd graph. They must be
    # re-encoded every epoch so gradients can update the specification encoder.
    spec_inputs = {
        fmt: torch.tensor(
            [spec_to_vector(format_spec(fmt))],
            dtype=torch.float32,
        )
        for fmt in formats
    }

    optimizer = torch.optim.AdamW(
        list(data_encoder.parameters())
        + list(spec_encoder.parameters())
        + list(decoder.parameters()),
        lr=2e-3,
    )
    loss_fn = nn.MSELoss()
    history: list[float] = []

    for _ in range(epochs):
        optimizer.zero_grad()
        data_z = data_encoder(x)
        losses = []

        for fmt in formats:
            spec_z = spec_encoder(spec_inputs[fmt]).expand(x.size(0), -1)
            prediction = decoder(data_z, spec_z)
            losses.append(loss_fn(prediction, x))

        loss = torch.stack(losses).mean()
        loss.backward()
        optimizer.step()
        history.append(float(loss.detach()))

    return {
        "data_encoder": data_encoder,
        "spec_encoder": spec_encoder,
        "decoder": decoder,
        "history": history,
        "formats": formats,
    }
