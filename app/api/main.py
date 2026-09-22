from typing import Any
import os
from time import perf_counter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from neurocodec.settlement.arc import ARC_MAINNET_CHAIN_ID, ARC_MAINNET_RPC, ARC_MAINNET_USDC, ArcSettlement
from neurocodec.settlement.receipts import create_receipt
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.translation.custom_spec import render_record, validate_custom_spec

app=FastAPI(title="NeuroCodec",version="1.1.0",description="Specification-conditioned neural translation with Arc Mainnet settlement.")
settlement=ArcSettlement()
adapter=CustomFormatAdapter()

class TranslateRequest(BaseModel):
    record:dict[str,Any]
    target_spec:dict[str,Any]
    adapt_steps:int=Field(default=0,ge=0,le=100)
    job_id:str|None=None

@app.get("/health")
def health():
    return {"status":"ok","service":"neurocodec","version":"1.1.0","arc":{"network":"arc-mainnet","chain_id":ARC_MAINNET_CHAIN_ID,"rpc":ARC_MAINNET_RPC,"usdc":ARC_MAINNET_USDC}}

@app.get("/config")
def config():
    return {"network":"arc-mainnet","chain_id":ARC_MAINNET_CHAIN_ID,"rpc":ARC_MAINNET_RPC,"usdc":ARC_MAINNET_USDC,"recipient":os.getenv("ARC_RECIPIENT_ADDRESS",""),"price_usdc":"0.01","mainnet_only":True}

@app.post("/translate")
def translate(req:TranslateRequest):
    start=perf_counter()
    try:
        spec=validate_custom_spec(req.target_spec)
        losses=adapter.adapt([req.record],spec,steps=req.adapt_steps) if req.adapt_steps else []
        latent=adapter.encode(req.record,spec)
        rendered=render_record(req.record,spec)
        receipt=create_receipt(req.job_id or "web-job",req.record,rendered,spec,model_version="neurocodec-1.1.0",chain="arc-mainnet")
        intent=settlement.payment_intent(receipt,"0.01",os.getenv("ARC_RECIPIENT_ADDRESS",""))
        return {"rendered":rendered,"latent":latent,"adaptation_loss":losses,"latency_ms":(perf_counter()-start)*1000,"receipt_digest":receipt.digest(),"receipt":receipt.__dict__,"arc":intent}
    except ValueError as exc: raise HTTPException(status_code=422,detail=str(exc)) from exc
    except RuntimeError as exc: raise HTTPException(status_code=503,detail=str(exc)) from exc
