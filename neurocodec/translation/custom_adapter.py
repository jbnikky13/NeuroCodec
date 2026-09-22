from __future__ import annotations
from .custom_spec import validate_custom_spec, render_record
from ..core.features import record_to_features
from ..translation.spec import spec_to_vector

class CustomFormatAdapter:
    """Lightweight deterministic adapter for the serverless Arc mini-app.

    The research PyTorch models remain available to training/benchmark code,
    but the Vercel request path intentionally does not import torch.
    """

    def adapt(self, records:list[dict], spec:dict, steps:int=8)->list[float]:
        validate_custom_spec(spec)
        if not records:
            raise ValueError("records cannot be empty")
        base = sum(sum(abs(x) for x in record_to_features(r)) for r in records) / len(records)
        return [base / (i + 1) for i in range(max(0, steps))]

    def encode(self, record:dict, spec:dict):
        validate_custom_spec(spec)
        features = record_to_features(record)
        spec_features = spec_to_vector(spec)
        # Lightweight shared latent representation: deterministic and
        # reproducible without the heavyweight ML runtime.
        return [round((a + b) / 2.0, 6) for a,b in zip(features, spec_features)]

    def translate(self, record:dict, spec:dict)->dict:
        return {
            "rendered": render_record(record, spec),
            "latent": self.encode(record, spec),
        }
