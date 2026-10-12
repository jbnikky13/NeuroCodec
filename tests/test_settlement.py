from neurocodec.settlement.arc import ArcSettlement
from neurocodec.settlement.receipts import create_receipt

VALID_ADDRESS = "0x1111111111111111111111111111111111111111"


def test_receipt_hashes_are_stable():
    a = create_receipt("job", {"a": 1}, "a=1", {"name": "x"}, model_version="v")
    b = create_receipt("job", {"a": 1}, "a=1", {"name": "x"}, model_version="v")
    assert a.input_hash == b.input_hash
    assert a.output_hash == b.output_hash
    assert a.spec_hash == b.spec_hash
    assert len(a.digest()) == 64


def test_payment_intent():
    receipt = create_receipt("job", {"a": 1}, "a=1", {"name": "x"})
    intent = ArcSettlement().payment_intent(receipt, "0.01", VALID_ADDRESS)
    assert intent["asset"] == "USDC"
    assert intent["receipt_digest"] == receipt.digest()
    assert intent["native_amount"] == "10000000000000000"
    assert intent["ready"] is True


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
