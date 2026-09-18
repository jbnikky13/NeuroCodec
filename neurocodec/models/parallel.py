from __future__ import annotations

import torch
from torch import nn


class Specialist(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, latent_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, latent_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ParallelEncoder(nn.Module):
    """Phase-1 parallel specialist encoder.

    The specialists currently consume fixed numeric feature vectors produced
    by the feature layer. Training is intentionally separated from encoding
    so experiments can swap feature extractors without changing the model.
    """

    def __init__(self, input_dim: int = 16, hidden_dim: int = 32, latent_dim: int = 16):
        super().__init__()
        self.structure = Specialist(input_dim, hidden_dim, latent_dim)
        self.semantic = Specialist(input_dim, hidden_dim, latent_dim)
        self.temporal = Specialist(input_dim, hidden_dim, latent_dim)
        self.fusion = nn.Sequential(
            nn.Linear(latent_dim * 3, latent_dim * 2),
            nn.GELU(),
            nn.Linear(latent_dim * 2, latent_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        parts = [
            self.structure(x),
            self.semantic(x),
            self.temporal(x),
        ]
        return self.fusion(torch.cat(parts, dim=-1))
