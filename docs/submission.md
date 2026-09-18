# NeuroCodec — Submission Package

## One-line concept

NeuroCodec is a specification-conditioned neural translation system that learns a shared representation from structured data and adapts to target formats described at runtime.

## What is novel in this implementation

The target format is treated as a machine-readable specification rather than only as a fixed codec identity. The system combines a parallel data encoder with a learned specification encoder and conditional decoder, then supports bounded online adaptation.

## Demonstration path

1. Open the interactive API/demo.
2. Provide a structured record.
3. Define a target format specification.
4. Translate the record.
5. Inspect the output, latency and verifiable receipt.
6. Optionally create an Arc settlement intent.

## Reproduce the final benchmark

```bash
python scripts/run_final_benchmark.py
```

The command writes `artifacts/final-benchmark.json`.

## Research claims and boundaries

NeuroCodec currently demonstrates:
- shared latent representation learning
- specification-conditioned translation
- adaptation to an unregistered custom format specification
- bounded online adaptation
- adversarial specification validation
- reproducible inference measurements
- cryptographically committed translation receipts

It does **not** claim that arbitrary binary formats can already be translated perfectly zero-shot. The current renderer and feature representation impose explicit limits. These limitations are part of the research record.

## Arc role

Arc is the settlement and verification boundary, not part of the neural network. A translation receipt hashes the input, output, target specification and model version. A settlement intent can reference that digest without placing private keys inside the model service.

## Evaluation checklist

- [ ] Run full CI
- [ ] Run final benchmark
- [ ] Confirm demo/API deployment
- [ ] Record benchmark artifact
- [ ] Verify receipt digest
- [ ] Verify Arc settlement intent without broadcasting funds
- [ ] Freeze the submission commit/tag

## Suggested judge demo

Use one familiar format first, then replace it with an unregistered format specification. Show that the same pipeline accepts the specification, adapts, produces a result and creates a verifiable receipt. Then show the robustness report and explain the explicit limitations.

## Reproducibility

All benchmark commands and tests are kept in the repository. Results should be reported from the actual run rather than from predetermined numbers.
