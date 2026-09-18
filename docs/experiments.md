# Experiments

### Baseline
- codec round-trip correctness
- latent dimensionality and numerical stability
- JSON, CSV and custom-format translation

### Held-out format experiment
Train on selected format pairs while withholding one target representation. Evaluate:
- field recovery
- type recovery
- value error
- structural similarity
- inference latency
- adaptation time

No universal-translation claim should be made until measurements support it.
