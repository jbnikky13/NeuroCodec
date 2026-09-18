from abc import ABC, abstractmethod
from typing import Any


class Codec(ABC):
    name: str

    @abstractmethod
    def encode(self, record: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, payload: str) -> dict[str, Any]:
        raise NotImplementedError
