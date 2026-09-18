import torch
from neurocodec.core.features import FEATURE_DIM,record_to_features
from neurocodec.models.parallel import ParallelEncoder
def test_parallel_encoder_shape():
    x=torch.tensor([record_to_features({"temperature":28.4,"location":"PH"})],dtype=torch.float32); y=ParallelEncoder()(x)
    assert y.shape==(1,16); assert torch.isfinite(y).all()
def test_feature_dimension(): assert len(record_to_features({"a":1}))==FEATURE_DIM
