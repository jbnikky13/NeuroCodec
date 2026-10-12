import json

import neurocodec.settlement.arc as arc_module
from neurocodec.settlement.arc import ArcSettlement
from neurocodec.settlement.receipts import create_receipt

VALID_ADDRESS = "0x1111111111111111111111111111111111111111"
TX_HASH = "0x" + "1" * 64
DIGEST = "a" * 64
SIGNATURE = "b" * 64


def test_receipt_hashes_are_stable():
    a = create_receipt("job", {"a": 1}, "a=1", {"name": "x"}, model_version="v")
    b = create_receipt("job", {"a": 1}, "a=1", {"name": "x"}, model_version="v")
    assert a.input_hash == b.input_hash
    assert a.output_hash == b.output_hash
    assert a.spec_hash == b.spec_hash
    assert len(a.digest()) == 64


def test_payment_intent(monkeypatch):
    monkeypatch.delenv("NEUROCODEC_RECEIPT_SECRET", raising=False)
    receipt = create_receipt("job", {"a": 1}, "a=1", {"name": "x"})
    intent = ArcSettlement().payment_intent(receipt, "0.01", VALID_ADDRESS)
    assert intent["asset"] == "USDC"
    assert intent["receipt_digest"] == receipt.digest()
    assert intent["native_amount"] == "10000000000000000"
    assert intent["ready"] is False  # signing secret is intentionally absent in unit tests


def test_payment_intent_rejects_invalid_recipient():
    receipt = create_receipt("job", {"a": 1}, "a=1", {"name": "x"})
    try:
        ArcSettlement().payment_intent(receipt, "0.01", "0xrecipient")
    except ValueError as exc:
        assert "valid EVM address" in str(exc)
    else:
        raise AssertionError("invalid recipient must be rejected")


def test_payment_intent_rejects_non_positive_amount():
    receipt = create_receipt("job", {"a": 1}, "a=1", {"name": "x"})
    for amount in ("0", "-0.01"):
        try:
            ArcSettlement().payment_intent(receipt, amount, VALID_ADDRESS)
        except ValueError as exc:
            assert "positive" in str(exc)
        else:
            raise AssertionError(f"amount {amount} must be rejected")


def test_verify_payment_confirms_matching_mined_transaction(monkeypatch):
    transaction = {
        "to": VALID_ADDRESS,
        "value": hex(10**16),
        "input": "0x",
        "chainId": hex(5042),
    }
    mined_receipt = {
        "transactionHash": TX_HASH,
        "status": "0x1",
        "blockNumber": "0x10",
    }

    def fake_rpc(_url, method, _params):
        if method == "eth_chainId":
            return hex(5042)
        if method == "eth_getTransactionByHash":
            return transaction
        if method == "eth_getTransactionReceipt":
            return mined_receipt
        raise AssertionError(f"unexpected RPC method: {method}")

    monkeypatch.setattr(arc_module, "_rpc_call", fake_rpc)
    result = ArcSettlement().verify_payment(TX_HASH, DIGEST, SIGNATURE, VALID_ADDRESS)
    assert result["verified"] is True
    assert result["status"] == "confirmed"
    assert result["block_number"] == "0x10"


def test_verify_payment_rejects_wrong_recipient(monkeypatch):
    transaction = {
        "to": "0x2222222222222222222222222222222222222222",
        "value": hex(10**16),
        "input": "0x",
        "chainId": hex(5042),
    }

    def fake_rpc(_url, method, _params):
        if method == "eth_chainId":
            return hex(5042)
        if method == "eth_getTransactionByHash":
            return transaction
        raise AssertionError(f"unexpected RPC method: {method}")

    monkeypatch.setattr(arc_module, "_rpc_call", fake_rpc)
    result = ArcSettlement().verify_payment(TX_HASH, DIGEST, SIGNATURE, VALID_ADDRESS)
    assert result["verified"] is False
    assert result["status"] == "recipient_mismatch"


def test_rpc_call_retries_transient_timeout(monkeypatch):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps({"jsonrpc": "2.0", "id": 1, "result": "0x13b2"}).encode()

    calls = {"count": 0}

    def flaky_urlopen(_request, timeout):
        assert timeout == arc_module.RPC_TIMEOUT_SECONDS
        calls["count"] += 1
        if calls["count"] == 1:
            raise TimeoutError("temporary timeout")
        return FakeResponse()

    monkeypatch.setattr(arc_module, "urlopen", flaky_urlopen)
    monkeypatch.setattr(arc_module, "sleep", lambda _seconds: None)

    assert arc_module._rpc_call(arc_module.ARC_MAINNET_RPC, "eth_chainId", []) == "0x13b2"
    assert calls["count"] == 2


def test_rpc_call_reports_clear_error_after_retries(monkeypatch):
    def always_timeout(_request, timeout):
        raise TimeoutError("temporary timeout")

    monkeypatch.setattr(arc_module, "urlopen", always_timeout)
    monkeypatch.setattr(arc_module, "sleep", lambda _seconds: None)

    try:
        arc_module._rpc_call(arc_module.ARC_MAINNET_RPC, "eth_chainId", [])
    except RuntimeError as exc:
        assert "failed after 2 attempts" in str(exc)
        assert "Do not submit another payment" in str(exc)
    else:
        raise AssertionError("RPC timeout must produce a clear RuntimeError")
