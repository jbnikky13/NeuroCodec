# Experiments

## Phase 1.5 — latent reconstruction baseline

A trainable parallel encoder/decoder learns to reconstruct deterministic feature representations from a shared latent space.

## Phase 2 — learned format decoder baseline

Separate learned decoder heads were introduced for JSON, CSV and PIPE.

## Phase 3 — held-out format experiment

One format is deliberately withheld from training to prevent accidental leakage.

## Phase 4 — format-specification conditioning

A target format is represented by a machine-readable specification and encoded into a learned vector.

## Phase 5 — live streaming and online adaptation

A bounded stream buffer and conservative recent-window adaptation loop were added.

## Phase 6 — unregistered custom format

The system can accept a runtime format specification without requiring a pre-registered codec.

## Phase 7 — robustness and adversarial benchmarking

Phase 7 adds a repeatable robustness suite covering:

- unseen Unicode separators
- multi-character delimiters
- delimiter collisions
- invalid empty separators
- invalid empty key/value delimiters
- output finiteness
- inference latency
- throughput
- aggregate pass rate

Run:

```bash
python scripts/run_robustness.py
```

The adversarial suite intentionally contains both valid and invalid specifications. A rejected invalid specification is a successful robustness outcome; therefore pass rate measures correct handling of test cases, not raw acceptance.

This phase does not claim superiority over conventional codecs. It creates measurable controls that can support that comparison later.

The next phase should expose the research pipeline through a production API and interactive demo, while preserving the benchmark suite as regression tests.
