from __future__ import annotations
from typing import Any

def validate_custom_spec(spec:dict[str,Any])->dict[str,Any]:
    required={"name","field_separator","key_value","strings","numbers"}
    missing=required-set(spec)
    if missing: raise ValueError(f"Missing specification fields: {sorted(missing)}")
    if not isinstance(spec["field_separator"],str) or not spec["field_separator"]:
        raise ValueError("field_separator must be a non-empty string")
    if not isinstance(spec["key_value"],str) or not spec["key_value"]:
        raise ValueError("key_value must be a non-empty string")
    return dict(spec)

def render_record(record:dict[str,Any],spec:dict[str,Any])->str:
    s=validate_custom_spec(spec)
    sep=s["field_separator"]; kv=s["key_value"]
    if sep in kv: raise ValueError("field_separator and key_value must differ")
    fields=[]
    for key,value in record.items():
        text=str(value).lower() if isinstance(value,bool) else str(value)
        if sep in text or kv in text:
            raise ValueError("record contains a value incompatible with the supplied specification")
        fields.append(f"{key}{kv}{text}")
    return sep.join(fields)
