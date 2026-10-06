from __future__ import annotations

from typing import Any

MAX_SPEC_NAME = 128
MAX_SEPARATOR = 16
MAX_KEY_VALUE = 16


def validate_custom_spec(spec: dict[str, Any]) -> dict[str, Any]:
    required = {"name", "field_separator", "key_value", "strings", "numbers"}
    missing = required - set(spec)
    if missing:
        raise ValueError(f"Missing specification fields: {sorted(missing)}")
    if not isinstance(spec.get("name"), str) or not spec["name"].strip():
        raise ValueError("name must be a non-empty string")
    if len(spec["name"]) > MAX_SPEC_NAME:
        raise ValueError("name is too long")
    if not isinstance(spec["field_separator"], str) or not spec["field_separator"]:
        raise ValueError("field_separator must be a non-empty string")
    if len(spec["field_separator"]) > MAX_SEPARATOR:
        raise ValueError("field_separator is too long")
    if not isinstance(spec["key_value"], str) or not spec["key_value"]:
        raise ValueError("key_value must be a non-empty string")
    if len(spec["key_value"]) > MAX_KEY_VALUE:
        raise ValueError("key_value is too long")
    if spec["field_separator"] == spec["key_value"]:
        raise ValueError("field_separator and key_value must differ")
    for field in ("strings", "numbers"):
        if not isinstance(spec[field], str) or not spec[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    return dict(spec)


def render_record(record: dict[str, Any], spec: dict[str, Any]) -> str:
    s = validate_custom_spec(spec)
    sep = s["field_separator"]
    kv = s["key_value"]
    fields = []

    for key, value in record.items():
        if not isinstance(key, str) or not key:
            raise ValueError("record keys must be non-empty strings")
        key_text = key
        text = str(value).lower() if isinstance(value, bool) else str(value)
        if any(token in key_text for token in (sep, kv)):
            raise ValueError("record key contains an incompatible separator")
        if any(token in text for token in (sep, kv)):
            raise ValueError("record contains a value incompatible with the supplied specification")
        fields.append(f"{key_text}{kv}{text}")

    return sep.join(fields)
