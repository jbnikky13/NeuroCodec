from __future__ import annotations

import json
import os
from time import perf_counter
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from neurocodec.settlement.arc import (
    ARC_MAINNET_CHAIN_ID,
    ARC_MAINNET_RPC,
    ARC_MAINNET_USDC,
    ArcSettlement,
)
from neurocodec.settlement.receipts import create_receipt
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.translation.custom_spec import render_record, validate_custom_spec

APP_VERSION = "1.2.0"
MAX_RECORD_BYTES = 256_000
MAX_SPEC_BYTES = 32_000

app = FastAPI(
    title="NeuroCodec",
    version=APP_VERSION,
    description="Specification-conditioned neural translation with Arc Mainnet settlement.",
)
settlement = ArcSettlement()
adapter = CustomFormatAdapter()


class TranslateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record: dict[str, Any]
    target_spec: dict[str, Any]
    adapt_steps: int = Field(default=0, ge=0, le=100)
    job_id: str | None = Field(default=None, max_length=128)

    @field_validator("record")
    @classmethod
    def validate_record(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("record cannot be empty")
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        if len(encoded.encode("utf-8")) > MAX_RECORD_BYTES:
            raise ValueError(f"record exceeds {MAX_RECORD_BYTES} bytes")
        return value

    @field_validator("target_spec")
    @classmethod
    def validate_spec_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        if len(encoded.encode("utf-8")) > MAX_SPEC_BYTES:
            raise ValueError(f"target_spec exceeds {MAX_SPEC_BYTES} bytes")
        return value


@app.get("/")
def root():
    return {
        "service": "neurocodec",
        "version": APP_VERSION,
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "neurocodec",
        "version": APP_VERSION,
        "arc": {
            "network": "arc-mainnet",
            "chain_id": ARC_MAINNET_CHAIN_ID,
            "rpc": ARC_MAINNET_RPC,
            "usdc": ARC_MAINNET_USDC,
        },
    }


@app.get("/config")
def config():
    recipient = os.getenv("ARC_RECIPIENT_ADDRESS", "")
    return {
        "network": "arc-mainnet",
        "chain_id": ARC_MAINNET_CHAIN_ID,
        "rpc": ARC_MAINNET_RPC,
        "usdc": ARC_MAINNET_USDC,
        "recipient": recipient,
        "price_usdc": "0.01",
        "mainnet_only": True,
        "payment_ready": bool(recipient),
    }


@app.get("/formats")
def formats():
    return {
        "formats": [
            {"name": "json", "kind": "registered", "description": "JSON object"},
            {"name": "csv", "kind": "registered", "description": "CSV records"},
            {"name": "pipe", "kind": "registered", "description": "key=value|key=value"},
            {"name": "custom", "kind": "specification-conditioned", "description": "User-defined separator and key/value syntax"},
        ]
    }


@app.post("/translate")
def translate(req: TranslateRequest):
    start = perf_counter()
    try:
        spec = validate_custom_spec(req.target_spec)
        losses = adapter.adapt([req.record], spec, steps=req.adapt_steps) if req.adapt_steps else []
        latent = adapter.encode(req.record, spec)
        rendered = render_record(req.record, spec)

        receipt = create_receipt(
            req.job_id or "web-job",
            req.record,
            rendered,
            spec,
            model_version=f"neurocodec-{APP_VERSION}",
            chain="arc-mainnet",
        )

        recipient = os.getenv("ARC_RECIPIENT_ADDRESS", "")
        intent = settlement.payment_intent(receipt, "0.01", recipient)

        return {
            "rendered": rendered,
            "latent": latent,
            "adaptation_loss": losses,
            "latency_ms": round((perf_counter() - start) * 1000, 3),
            "receipt_digest": receipt.digest(),
            "receipt": receipt.__dict__,
            "arc": intent,
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
