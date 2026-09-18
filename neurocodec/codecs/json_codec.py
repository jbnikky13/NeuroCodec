import json
from typing import Any
from .base import Codec


class JsonCodec(Codec):
    name = "json"

    def encode(self, record: dict[str, Any]) -> str:
        return json.dumps(record, separators=(",", ":"), sort_keys=True)

    def decode(self, payload: str) -> dict[str, Any]:
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("JSON payload must decode to an object")
        return value
