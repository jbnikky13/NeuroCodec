import csv
import io
import json
from typing import Any
from .base import Codec


class CsvCodec(Codec):
    name = "csv"

    def encode(self, record: dict[str, Any]) -> str:
        keys = list(record.keys())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerow({k: self._scalar(v) for k, v in record.items()})
        return output.getvalue().strip()

    def decode(self, payload: str) -> dict[str, Any]:
        rows = list(csv.DictReader(io.StringIO(payload)))
        if len(rows) != 1:
            raise ValueError("CSV payload must contain exactly one data row")
        return {k: self._restore(v) for k, v in rows[0].items()}

    @staticmethod
    def _scalar(value: Any) -> str:
        if isinstance(value, (dict, list)):
            return json.dumps(value, separators=(",", ":"), sort_keys=True)
        return str(value)

    @staticmethod
    def _restore(value: str) -> Any:
        for parser in (int, float):
            try:
                return parser(value)
            except ValueError:
                pass
        if value in ("true", "false"):
            return value == "true"
        return value
