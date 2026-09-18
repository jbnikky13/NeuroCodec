from __future__ import annotations
import random
from typing import Any
def make_record(rng:random.Random)->dict[str,Any]:
    return {"temperature":round(rng.uniform(18,40),2),"location":rng.choice(["PH","LAG","ABJ","KAN"]),"timestamp":rng.randint(1700000000,1800000000),"status":rng.choice(["OK","WARN","FAIL"]),"pressure":round(rng.uniform(0.8,1.2),3)}
def make_dataset(n:int=256,seed:int=42)->list[dict[str,Any]]:
    rng=random.Random(seed); return [make_record(rng) for _ in range(n)]
