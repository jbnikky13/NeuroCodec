from __future__ import annotations
import json
from pathlib import Path
from time import perf_counter
from neurocodec.data.generator import make_dataset
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.translation.custom_spec import render_record
from neurocodec.validation.robustness import benchmark_model,check_spec,aggregate

def fidelity(adapter,records,spec):
    # Feature-space reconstruction is a diagnostic, not a claim of semantic equivalence.
    import torch
    from neurocodec.core.features import record_to_features
    import torch.nn.functional as F
    with torch.inference_mode():
        errors=[]
        finite=0
        for r in records:
            p=adapter.encode(r,spec)
            target=torch.tensor(record_to_features(r),dtype=torch.float32)
            if bool(torch.isfinite(p).all()): finite+=1
            errors.append(float(F.mse_loss(p,target)))
    mse=sum(errors)/max(1,len(errors))
    return {"feature_mse":mse,"finite_rate":finite/max(1,len(records))}

def roundtrip_format_validity(records,spec):
    valid=0
    for r in records:
        try:
            render_record(r,spec); valid+=1
        except (ValueError,TypeError): pass
    return valid/max(1,len(records))

def main():
    records=make_dataset(32,2026)
    spec={"name":"neuropipe-v1","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain","nested":"unsupported"}
    adapter=CustomFormatAdapter()
    before=benchmark_model(adapter,records,spec)
    before_fidelity=fidelity(adapter,records,spec)
    losses=adapter.adapt(records,spec,steps=8)
    after=benchmark_model(adapter,records,spec)
    after_fidelity=fidelity(adapter,records,spec)
    format_validity=roundtrip_format_validity(records,spec)
    robustness_specs=[
      spec,
      {**spec,"name":"alternate-separator","field_separator":"|"},
      {**spec,"name":"missing-name","name":None},
      {**spec,"name":"empty-separator","field_separator":""},
      {**spec,"name":"separator-in-kv","field_separator":"=>"},
      {**spec,"name":"empty-key-value","key_value":""},
    ]
    robustness=[check_spec(s) for s in robustness_specs]
    report={
      "benchmark":"neurocodec-final",
      "dataset_size":len(records),
      "spec":spec,
      "before":before,
      "after":after,
      "adaptation":{"steps":len(losses),"initial_loss":losses[0] if losses else None,"final_loss":losses[-1] if losses else None,"loss_reduction":(losses[0]-losses[-1])/losses[0] if losses else None,"loss_history":losses},
      "fidelity":{"before":before_fidelity,"after":after_fidelity,"format_validity_rate":format_validity},
      "robustness":aggregate(robustness),
      "interpretation":{"feature_mse":"Diagnostic feature-space reconstruction error; lower is better.","format_validity_rate":"Fraction of benchmark records accepted by the target specification renderer.","robustness_note":"Includes valid and intentionally invalid specifications; rejection of invalid specifications is a pass."}
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/final-benchmark.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
