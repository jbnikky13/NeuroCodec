from neurocodec.data.generator import make_dataset
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.translation.custom_spec import render_record

NOVEL_SPEC={
    "name":"neuropipe-v1",
    "field_separator":"~",
    "key_value":"=>",
    "strings":"plain",
    "numbers":"plain",
    "nested":"unsupported",
}

def main():
    records=make_dataset(16,2026)
    adapter=CustomFormatAdapter()
    before=adapter.encode(records[0],NOVEL_SPEC)
    losses=adapter.adapt(records,NOVEL_SPEC,steps=8)
    after=adapter.encode(records[0],NOVEL_SPEC)
    rendered=render_record(records[0],NOVEL_SPEC)
    print({
        "experiment":"phase-6-unregistered-format",
        "registered_codec":False,
        "format_spec":NOVEL_SPEC,
        "sample_before_vector":before.tolist(),
        "adaptation_losses":losses,
        "sample_after_vector":after.tolist(),
        "rendered_target":rendered,
    })

if __name__=="__main__":main()
