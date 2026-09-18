from __future__ import annotations
from dataclasses import dataclass
from time import time
from typing import Any

@dataclass(frozen=True)
class StreamEvent:
    record: dict[str, Any]
    received_at: float

class StreamBuffer:
    def __init__(self,max_size:int=128):
        if max_size < 1: raise ValueError("max_size must be positive")
        self.max_size=max_size
        self._items:list[StreamEvent]=[]
    def push(self,record:dict[str,Any],received_at:float|None=None)->StreamEvent:
        event=StreamEvent(record=dict(record),received_at=time() if received_at is None else received_at)
        self._items.append(event)
        if len(self._items)>self.max_size: self._items.pop(0)
        return event
    def snapshot(self)->list[StreamEvent]: return list(self._items)
    def __len__(self): return len(self._items)
