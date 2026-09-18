from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Any
import math
import torch
from ..translation.custom_spec import validate_custom_spec,render_record

@dataclass
class RobustnessResult:
    name:str
    passed:bool
    error:str|None
    latency_ms:float

def check_spec(spec:dict[str,Any])->RobustnessResult:
    start=perf_counter()
    try:
        validate_custom_spec(spec)
        render_record({"a":1,"b":"x"},spec)
        return RobustnessResult(spec.get("name","unnamed"),True,None,(perf_counter()-start)*1000)
    except (ValueError,TypeError) as exc:
        return RobustnessResult(spec.get("name","unnamed"),False,str(exc),(perf_counter()-start)*1000)

def benchmark_model(adapter,records,spec)->dict[str,float]:
    start=perf_counter()
    with torch.inference_mode():
        preds=[adapter.encode(r,spec) for r in records]
    elapsed=perf_counter()-start
    finite=all(bool(torch.isfinite(p).all()) for p in preds)
    return {"records":float(len(records)),"latency_ms":elapsed*1000/max(1,len(records)),"records_per_second":len(records)/max(elapsed,1e-9),"finite_outputs":float(finite)}

def aggregate(results:list[RobustnessResult])->dict[str,float]:
    if not results:return {"cases":0.0,"pass_rate":0.0,"mean_latency_ms":0.0}
    return {"cases":float(len(results)),"pass_rate":sum(r.passed for r in results)/len(results),"mean_latency_ms":sum(r.latency_ms for r in results)/len(results)}
