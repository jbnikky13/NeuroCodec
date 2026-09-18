from neurocodec.settlement.receipts import create_receipt
from neurocodec.settlement.arc import ArcSettlement
def test_receipt_hashes_are_stable():
    a=create_receipt("job",{"a":1},"a=1",{"name":"x"},model_version="v")
    b=create_receipt("job",{"a":1},"a=1",{"name":"x"},model_version="v")
    assert a.input_hash==b.input_hash and a.output_hash==b.output_hash and a.spec_hash==b.spec_hash
    assert len(a.digest())==64
def test_payment_intent():
    r=create_receipt("job",{"a":1},"a=1",{"name":"x"})
    i=ArcSettlement().payment_intent(r,"0.01","0xrecipient")
    assert i["asset"]=="USDC" and i["receipt_digest"]==r.digest()
