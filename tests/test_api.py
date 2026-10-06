from fastapi.testclient import TestClient

from neurocodec.api.app import app

client = TestClient(app)
SPEC = {
    "name": "test-v1",
    "field_separator": "~",
    "key_value": "=>",
    "strings": "plain",
    "numbers": "plain",
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_and_formats():
    assert client.get("/").status_code == 200
    payload = client.get("/formats").json()
    assert {item["name"] for item in payload["formats"]} >= {"json", "csv", "pipe", "custom"}


def test_translate_without_payment_configuration():
    response = client.post(
        "/translate",
        json={"record": {"temperature": 20.0, "location": "PH", "timestamp": 1}, "target_spec": SPEC},
    )
    assert response.status_code == 200
    body = response.json()
    assert "temperature=>20.0" in body["rendered"]
    assert len(body["latent"]) == 16
    assert body["arc"]["ready"] is False


def test_invalid_spec():
    response = client.post("/translate", json={"record": {"a": 1}, "target_spec": {"name": "bad"}})
    assert response.status_code == 422


def test_oversized_record():
    response = client.post(
        "/translate",
        json={"record": {"blob": "x" * 300_000}, "target_spec": SPEC},
    )
    assert response.status_code == 422
