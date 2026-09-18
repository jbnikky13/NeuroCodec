from __future__ import annotations

import hashlib
import json
import math
from typing import Any

FEATURE_DIM = 16


def _stable_number(value: Any) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return max(-1.0, min(1.0, float(value) / (abs(float(value)) + 1.0)))
    digest = hashlib.sha256(str(value).encode()).digest()
    return int.from_bytes(digest[:4], "big") / 2**32 * 2 - 1


def record_to_features(record: dict[str, Any]) -> list[float]:
    """Create a deterministic starter feature vector for the neural model.

    This is a research baseline, not a learned semantic tokenizer.
    """
    keys = sorted(record)
    type_counts = {
        "number": sum(isinstance(v, (int, float)) and not isinstance(v, bool) for v in record.values()),
        "text": sum(isinstance(v, str) for v in record.values()),
        "bool": sum(isinstance(v, bool) for v in record.values()),
        "nested": sum(isinstance(v, (dict, list)) for v in record.values()),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), default=str)
    values = [
        min(len(record) / 32.0, 1.0),
        min(len(keys) / 32.0, 1.0),
        type_counts["number"] / 32.0,
        type_counts["text"] / 32.0,
        type_counts["bool"] / 32.0,
        type_counts["nested"] / 32.0,
        min(len(canonical) / 2048.0, 1.0),
        sum(len(k) for k in keys) / max(1.0, len(keys) * 64.0),
    ]
    values.extend(_stable_number(record[k]) for k in keys[:8])
    return (values + [0.0] * FEATURE_DIM)[:FEATURE_DIM]
