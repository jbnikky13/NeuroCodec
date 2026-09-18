from __future__ import annotations
import hashlib, json
from typing import Any

def format_spec(format_name:str)->dict[str,Any]:
    specs={
      "json":{"name":"json","container":"object","field_separator":",","key_value":"colon","strings":"quoted","numbers":"native","nested":"supported"},
      "csv":{"name":"csv","container":"rows","field_separator":",","key_value":"header","strings":"plain","numbers":"textual","nested":"escaped"},
      "pipe":{"name":"pipe","container":"fields","field_separator":"|","key_value":"=","strings":"plain","numbers":"plain","nested":"unsupported"},
    }
    try:return specs[format_name]
    except KeyError as exc:raise ValueError(f"Unsupported format specification: {format_name}") from exc

def spec_to_vector(spec:dict[str,Any],dim:int=16)->list[float]:
    text=json.dumps(spec,sort_keys=True,separators=(",",":"))
    digest=hashlib.sha256(text.encode()).digest()
    return [b/255.0 for b in digest[:dim]]
