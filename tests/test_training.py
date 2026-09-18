import torch
from neurocodec.training.baseline import train_autoencoder
from neurocodec.validation.metrics import reconstruction_metrics
def test_training_reduces_loss():
    _,history=train_autoencoder(epochs=12)
    assert len(history)==12
    assert history[-1] < history[0]
def test_metrics():
    assert reconstruction_metrics([0,1],[0,0])["mse"]==0.5
