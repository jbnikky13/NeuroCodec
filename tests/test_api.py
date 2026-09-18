from fastapi.testclient import TestClient
from neurocodec.api.app import app

client=TestClient(app)
SPEC={"name":"test-v1","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain"}

def test_health():
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"

def test_translate():
    r=client.post("/translate",json={"record":{"temperature":20.0,"location":"PH","timestamp":1},"target_spec":SPEC})
    assert r.status_code==200
    assert "temperature=>20.0" in r.json()["rendered"]

def test_invalid_spec():
    r=client.post("/translate",json={"record":{"a":1},"target_spec":{"name":"bad"}})
    assert r.status_code==422
