from neurocodec.streaming.buffer import StreamBuffer
from neurocodec.streaming.online import OnlineAdapter
from neurocodec.streaming.metrics import benchmark_prediction

def test_buffer_is_bounded():
    b=StreamBuffer(2); b.push({"x":1}); b.push({"x":2}); b.push({"x":3})
    assert len(b)==2 and b.snapshot()[0].record["x"]==2

def test_online_adaptation_improves_loss():
    adapter=OnlineAdapter()
    records=[{"temperature":20.0,"location":"PH","timestamp":1},{"temperature":25.0,"location":"LAG","timestamp":2}]
    history=adapter.adapt(records,"json",steps=4)
    assert len(history)==4 and history[-1] <= history[0]

def test_stream_benchmark():
    adapter=OnlineAdapter()
    records=[{"temperature":20.0,"location":"PH","timestamp":1}]
    result=benchmark_prediction(adapter,records,"json")
    assert result["records"]==1
    assert result["latency_ms"] >= 0
