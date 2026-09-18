from __future__ import annotations

import torch

from ..codecs.registry import get_codec
from ..models.parallel import ParallelEncoder
from .features import record_to_features


class NeuroTranslator:
    """High-level Phase-1 translation service.

    The current baseline preserves information by decoding into a canonical
    record and re-encoding with the target codec, while also producing the
    learned latent representation. This clean separation lets later trained
    decoders replace the canonical bridge without changing the API.
    """

    def __init__(self, model: ParallelEncoder | None = None):
        self.model = model or ParallelEncoder()
        self.model.eval()

    @torch.inference_mode()
    def latent(self, record: dict) -> list[float]:
        x = torch.tensor([record_to_features(record)], dtype=torch.float32)
        return self.model(x)[0].tolist()

    def translate(self, payload: str, source: str, target: str) -> dict:
        source_codec = get_codec(source)
        target_codec = get_codec(target)
        record = source_codec.decode(payload)
        vector = self.latent(record)
        output = target_codec.encode(record)
        return {
            "source_format": source_codec.name,
            "target_format": target_codec.name,
            "output": output,
            "latent": vector,
            "field_count": len(record),
        }
