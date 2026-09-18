# Experiments

## Phase 1.5 — latent reconstruction baseline

A trainable parallel encoder/decoder learns to reconstruct deterministic feature representations from a shared latent space.

## Phase 2 — learned format decoder baseline

Separate learned decoder heads were introduced for JSON, CSV and PIPE.

## Phase 3 — held-out format experiment

One format is deliberately withheld from training to prevent accidental leakage.

## Phase 4 — format-specification conditioning

NeuroCodec now represents a target format through an explicit machine-readable specification and encodes that specification into a learned vector.

Architecture:

```
Input data ──> Data Encoder ──┐
                              ├─> Conditional Decoder ─> reconstructed signal
Format specification ─> Spec Encoder ─┘
```

Run:

```bash
python scripts/train_spec_conditioned.py
```

The specification currently describes container, separators, key/value rules, string/number handling and nesting. The specification encoder is deliberately deterministic at the input boundary so future experiments can replace it with a learned tokenizer or schema parser.

### Research significance

The model is no longer tied to one decoder per named format. In principle, a new format can be described by a specification and supplied to the same conditional decoder.

This is **not yet proof of arbitrary unseen-format generation**. The next experiment should hold out a format specification during training and evaluate whether a sufficiently expressive specification produces useful reconstruction.


## Phase 5 — live streaming and online adaptation

Phase 5 introduces a bounded stream buffer and a conservative online adaptation loop.

Architecture:

```
live records → bounded buffer → feature encoder
                               ↓
                         shared latent
                               ↓
format specification → spec encoder
                               ↓
                       conditional decoder
```

Run:

```bash
python scripts/run_live_demo.py
```

The demo reports:
- pre-adaptation reconstruction error
- online adaptation loss history
- post-adaptation reconstruction error
- throughput
- per-record latency
- bounded stream size

The adapter operates on a bounded recent window and updates only its supplied model objects. It does not claim continual learning or production streaming guarantees yet.

The next phase should introduce genuinely novel/custom format specifications and test whether the model can adapt to them without a pre-registered format decoder.
