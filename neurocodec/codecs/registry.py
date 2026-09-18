from .base import Codec
from .json_codec import JsonCodec
from .csv_codec import CsvCodec
from .custom_codec import PipeCodec

CODECS: dict[str, Codec] = {
    "json": JsonCodec(),
    "csv": CsvCodec(),
    "pipe": PipeCodec(),
}


def get_codec(name: str) -> Codec:
    try:
        return CODECS[name.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported codec: {name}") from exc
