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



def test_formats_distinguish_web_api_from_research_codecs():
    payload = client.get("/formats").json()
    formats = {item["name"]: item for item in payload["formats"]}
    assert formats["custom"]["available_in_web_api"] is True
    assert formats["custom"]["endpoint"] == "/translate"
    assert formats["json"]["available_in_web_api"] is False
    assert formats["csv"]["available_in_web_api"] is False
    assert formats["pipe"]["available_in_web_api"] is False


def test_translation_returns_signed_receipt_when_secret_is_configured(monkeypatch):
    monkeypatch.setenv("NEUROCODEC_RECEIPT_SECRET", "unit-test-secret")
    monkeypatch.setenv("ARC_RECIPIENT_ADDRESS", "0x1111111111111111111111111111111111111111")
    response = client.post(
        "/translate",
        json={"record": {"temperature": 20}, "target_spec": SPEC},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["receipt_digest"]) == 64
    assert len(body["receipt_signature"]) == 64
    assert body["arc"]["ready"] is True


def test_payment_verification_rejects_invalid_receipt_signature(monkeypatch):
    monkeypatch.setenv("ARC_RECIPIENT_ADDRESS", "0x1111111111111111111111111111111111111111")
    monkeypatch.setenv("NEUROCODEC_RECEIPT_SECRET", "unit-test-secret")
    response = client.post(
        "/verify-payment",
        json={
            "transaction_hash": "0x" + "1" * 64,
            "receipt_digest": "a" * 64,
            "receipt_signature": "b" * 64,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Receipt signature is invalid."



def test_payment_verification_accepts_valid_signed_receipt(monkeypatch):
    from neurocodec.api.app import _receipt_signature, settlement

    monkeypatch.setenv("ARC_RECIPIENT_ADDRESS", "0x1111111111111111111111111111111111111111")
    monkeypatch.setenv("NEUROCODEC_RECEIPT_SECRET", "unit-test-secret")
    digest = "a" * 64
    signature = _receipt_signature(digest, "unit-test-secret")
    monkeypatch.setattr(
        settlement,
        "verify_payment",
        lambda *args, **kwargs: {
            "verified": True,
            "status": "confirmed",
            "transaction_hash": args[0],
        },
    )
    response = client.post(
        "/verify-payment",
        json={
            "transaction_hash": "0x" + "1" * 64,
            "receipt_digest": digest,
            "receipt_signature": signature,
        },
    )
    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_payment_verification_rejects_malformed_digest(monkeypatch):
    monkeypatch.setenv("ARC_RECIPIENT_ADDRESS", "0x1111111111111111111111111111111111111111")
    monkeypatch.setenv("NEUROCODEC_RECEIPT_SECRET", "unit-test-secret")
    response = client.post(
        "/verify-payment",
        json={
            "transaction_hash": "0x" + "1" * 64,
            "receipt_digest": "z" * 64,
            "receipt_signature": "b" * 64,
        },
    )
    assert response.status_code == 422
    assert "receipt_digest" in response.json()["detail"]
