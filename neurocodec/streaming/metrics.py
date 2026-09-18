from __future__ import annotations
from time import perf_counter
import torch
from ..core.features import record_to_features
from ..validation.format_metrics import vector_metrics

def benchmark_prediction(adapter,records,target_format):
    if not records: raise ValueError("records cannot be empty")
    start=perf_counter()
    preds=[adapter.predict(r,target_format) for r in records]
    elapsed=perf_counter()-start
    target=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    pred=torch.stack(preds)
    metrics=vector_metrics(target,pred)
    return {**metrics,"records":len(records),"total_seconds":elapsed,"records_per_second":len(records)/max(elapsed,1e-9),"latency_ms":elapsed/len(records)*1000}
