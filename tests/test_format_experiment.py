from neurocodec.training.format_experiment import train_format_experiment
def test_format_decoder_training_improves():
    _,history=train_format_experiment(epochs=12)
    assert len(history)==12
    assert history[-1] < history[0]
