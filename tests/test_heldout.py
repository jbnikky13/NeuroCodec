from neurocodec.training.heldout import train_heldout_experiment
def test_heldout_excludes_target_decoder():
    r=train_heldout_experiment(held_out="pipe",epochs=8)
    assert "pipe" not in r["decoders"]
    assert set(r["decoders"])=={"json","csv"}
    assert r["history"][-1]<r["history"][0]
