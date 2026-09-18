from neurocodec.data.generator import make_dataset
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.translation.custom_spec import render_record,validate_custom_spec

SPEC={"name":"novel-v1","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain"}

def test_custom_spec_renders_without_registered_codec():
    record={"temperature":20.5,"location":"PH","timestamp":1}
    output=render_record(record,SPEC)
    assert "temperature=>20.5" in output and "~location=>PH~" in "~"+output+"~"

def test_custom_adaptation_improves():
    adapter=CustomFormatAdapter()
    history=adapter.adapt(make_dataset(8,11),SPEC,steps=6)
    assert len(history)==6 and history[-1] <= history[0]

def test_spec_validation():
    try: validate_custom_spec({"name":"bad"})
    except ValueError: return
    raise AssertionError("invalid specification should fail")
