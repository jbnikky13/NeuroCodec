from __future__ import annotations
from time import perf_counter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from ..data.generator import make_dataset
from ..translation.custom_spec import validate_custom_spec, render_record
from ..translation.custom_adapter import CustomFormatAdapter

app=FastAPI(title="NeuroCodec API",version="0.8.0",description="Format-independent neural translation research API")
adapter=CustomFormatAdapter()

class TranslateRequest(BaseModel):
    record:dict
    target_spec:dict
    adapt_steps:int=Field(default=0,ge=0,le=100)

class TranslateResponse(BaseModel):
    rendered:str
    latent:list[float]
    adaptation_loss:list[float]
    latency_ms:float

@app.get("/health")
def health(): return {"status":"ok","service":"neurocodec"}

@app.get("/formats")
def formats():
    return {"registered": ["json","csv","pipe"], "supports_custom_spec": True}

@app.post("/translate",response_model=TranslateResponse)
def translate(req:TranslateRequest):
    start=perf_counter()
    try: spec=validate_custom_spec(req.target_spec)
    except ValueError as exc: raise HTTPException(status_code=422,detail=str(exc))
    losses=[]
    if req.adapt_steps:
        losses=adapter.adapt([req.record],spec,steps=req.adapt_steps)
    latent=adapter.encode(req.record,spec)
    rendered=render_record(req.record,spec)
    return {"rendered":rendered,"latent":latent.tolist(),"adaptation_loss":losses,"latency_ms":(perf_counter()-start)*1000}

@app.get("/demo/sample")
def sample():
    record=make_dataset(1,2026)[0]
    spec={"name":"neuropipe-v1","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain"}
    return {"record":record,"target_spec":spec,"rendered":render_record(record,spec)}
