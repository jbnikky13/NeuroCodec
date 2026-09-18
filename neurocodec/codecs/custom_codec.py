from typing import Any
from .base import Codec


class PipeCodec(Codec):
    """Small deliberately custom format used for translation experiments.

    Example: temperature=28.4|location=PH|timestamp=1758211200
    """

    name = "pipe"

    def encode(self, record: dict[str, Any]) -> str:
        return "|".join(f"{key}={record[key]}" for key in record)

    def decode(self, payload: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for item in payload.split("|"):
            key, sep, value = item.partition("=")
            if not sep or not key:
                raise ValueError(f"Invalid pipe field: {item!r}")
            result[key] = self._restore(value)
        return result

    @staticmethod
    def _restore(value: str) -> Any:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
