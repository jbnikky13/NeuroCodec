from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from neurocodec.core.translator import NeuroTranslator

app = FastAPI(
    title="NeuroCodec",
    version="0.1.0",
    description="Experimental neural translation between structured data representations.",
)
translator = NeuroTranslator()


class TranslateRequest(BaseModel):
    payload: str = Field(min_length=1)
    source_format: Literal["json", "csv", "pipe"]
    target_format: Literal["json", "csv", "pipe"]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/translate")
def translate(request: TranslateRequest) -> dict:
    try:
        return translator.translate(
            request.payload,
            request.source_format,
            request.target_format,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
