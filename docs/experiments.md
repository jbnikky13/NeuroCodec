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

A bounded stream buffer and conservative recent-window adaptation loop were added. Latency, throughput and pre/post adaptation error can now be measured.

## Phase 6 — unregistered custom format

Phase 6 removes the assumption that a target format must exist in the codec registry.

The experiment defines a novel format at runtime:

- field separator: `~`
- key/value delimiter: `=>`
- plain strings
- plain numbers
- no nested structures

No codec named `neuropipe-v1` is registered.

Run:

```bash
python scripts/run_custom_format.py
```

The system receives only the format specification and adapts its shared model using example records. A deterministic renderer provides a ground-truth textual representation for verification.

### What this proves—and what it does not

This demonstrates the software path for an unregistered specification and measures adaptation of the shared representation. It does **not** yet prove zero-shot arbitrary byte-level generation. The decoder still operates in the learned feature space, while the deterministic renderer produces the exact textual output.

Phase 7 should introduce strict benchmarks against direct pair-specific models and adversarial specifications, including unseen separators, ordering rules, escaping and type constraints.
