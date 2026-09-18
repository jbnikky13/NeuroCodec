from __future__ import annotations
import math
def reconstruction_metrics(target:list[float],pred:list[float])->dict[str,float]:
    if len(target)!=len(pred) or not target: raise ValueError("Vectors must have equal non-zero length")
    mse=sum((a-b)**2 for a,b in zip(target,pred))/len(target)
    mae=sum(abs(a-b) for a,b in zip(target,pred))/len(target)
    rmse=math.sqrt(mse)
    return {"mse":mse,"mae":mae,"rmse":rmse}
