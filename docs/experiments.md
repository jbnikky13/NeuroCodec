# Experiments

## Phase 1.5 — latent reconstruction baseline

A trainable parallel encoder/decoder learns to reconstruct deterministic feature representations from a shared latent space.

## Phase 2 — learned format decoder baseline

Separate learned decoder heads were introduced for JSON, CSV and PIPE. The heads reconstruct format-specific numeric targets.

## Phase 3 — held-out format experiment

The first controlled generalization experiment deliberately withholds one format from training.

Default experiment:

```
TRAIN: JSON + CSV
HOLD OUT: PIPE
```

Run:

```bash
python scripts/run_heldout_experiment.py
```

The held-out format still has a target representation generated from its codec, but **no decoder for that format is trained**. This prevents accidental leakage.

### Important interpretation

A held-out target is not automatically proof of zero-shot translation. The current phase establishes the experimental split and measures the learned representation. A genuine zero-shot decoder requires an explicit mechanism for mapping an unseen format description/specification into the latent/decoder space.

That mechanism is the next research step.

Metrics:
- MSE
- MAE
- RMSE
- cosine similarity
- inference latency
- parameter count

A direct pair-specific baseline will be added before making any comparative claim.
