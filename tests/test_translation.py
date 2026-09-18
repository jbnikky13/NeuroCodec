from neurocodec.core.translator import NeuroTranslator
def test_translation_preserves_fields():
    r=NeuroTranslator().translate("temperature=28.4|location=PH|timestamp=1758211200","pipe","json")
    assert r["target_format"]=="json" and '"temperature":28.4' in r["output"] and r["field_count"]==3 and len(r["latent"])==16
