from neurocodec.data.generator import make_dataset
from neurocodec.streaming.buffer import StreamBuffer
from neurocodec.streaming.online import OnlineAdapter
from neurocodec.streaming.metrics import benchmark_prediction

def main():
    stream=StreamBuffer(max_size=32)
    records=make_dataset(12,2026)
    for record in records: stream.push(record)
    adapter=OnlineAdapter()
    before=benchmark_prediction(adapter,records[:4],"json")
    losses=adapter.adapt([e.record for e in stream.snapshot()],"json",steps=3)
    after=benchmark_prediction(adapter,records[:4],"json")
    print({"phase":"5-live-online-adaptation","before":before,"adaptation_losses":losses,"after":after,"buffer_size":len(stream)})
if __name__=="__main__": main()
