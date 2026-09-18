from neurocodec.translation.spec import format_spec, spec_to_vector
from neurocodec.translation.spec_encoder import FormatSpecEncoder
from neurocodec.training.spec_experiment import train_spec_conditioned


def test_specs_are_distinct():
    assert spec_to_vector(format_spec("json")) != spec_to_vector(format_spec("pipe"))


def test_spec_encoder_shape():
    encoder = FormatSpecEncoder()
    vector = encoder.encode_spec(format_spec("json"))
    assert tuple(vector.shape) == (16,)


def test_spec_training_improves():
    result = train_spec_conditioned(epochs=8)
    assert len(result["history"]) == 8
    assert result["history"][-1] < result["history"][0]
