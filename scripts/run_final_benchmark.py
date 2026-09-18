from __future__ import annotations
import json
from pathlib import Path
from neurocodec.data.generator import make_dataset
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.validation.adversarial import run_adversarial_suite
from neurocodec.validation.robustness import benchmark_model

def main():
    records=make_dataset(32,2026)
    spec={"name":"neuropipe-v1","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain","nested":"unsupported"}
    adapter=CustomFormatAdapter()
    before=benchmark_model(adapter,records,spec)
    losses=adapter.adapt(records,spec,steps=8)
    after=benchmark_model(adapter,records,spec)
    _,robustness=run_adversarial_suite()
    report={"benchmark":"neurocodec-final","dataset_size":len(records),"spec":spec,"before":before,"adaptation_losses":losses,"after":after,"robustness":robustness}
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/final-benchmark.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
