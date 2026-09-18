from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import hashlib,json
from typing import Any
@dataclass(frozen=True)
class TranslationReceipt:
    job_id:str; input_hash:str; output_hash:str; spec_hash:str; model_version:str; created_at:str; chain:str="arc"
    def canonical(self): return json.dumps(asdict(self),sort_keys=True,separators=(",",":"))
    def digest(self): return hashlib.sha256(self.canonical().encode()).hexdigest()
def _hash(v:Any)->str: return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
def create_receipt(job_id,input_payload,output_payload,target_spec,model_version="neurocodec-0.8.0",chain="arc"):
    return TranslationReceipt(job_id,_hash(input_payload),_hash(output_payload),_hash(target_spec),model_version,datetime.now(timezone.utc).isoformat(),chain)
