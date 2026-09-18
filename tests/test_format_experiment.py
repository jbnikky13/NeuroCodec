from neurocodec.training.format_experiment import train_format_experiment
def test_format_decoder_training_improves():
    _,h=train_format_experiment(epochs=12)
    assert len(h)==12 and h[-1]<h[0]
