# Experiments

## Phase 1.5 — latent reconstruction baseline

A trainable parallel encoder/decoder learns to reconstruct deterministic feature representations from the shared latent space.

## Phase 2 — learned format decoder baseline

Phase 2 introduces separate learned decoder heads for JSON, CSV and the custom pipe format. The current heads reconstruct a common feature target. This is an intermediate control experiment: it tests whether multiple format-specific heads can share one representation without changing the encoder.

Run:

```bash
python scripts/train_format_experiment.py
```

### Important limitation

The current heads do not yet emit raw JSON/CSV/pipe bytes. They reconstruct the canonical feature space. This prevents us from confusing an architectural baseline with actual format generation.

### Next: held-out format experiment

The next model will train against codec-specific representations, deliberately withhold one target representation, and evaluate whether the shared latent space supports reconstruction of that unseen representation.

Report:
- field recovery
- type recovery
- value error
- structural similarity
- latent reconstruction error
- inference latency
- adaptation/training time

A direct pair-specific model will be kept as a baseline so any improvement can be compared fairly.
