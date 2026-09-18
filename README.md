# NeuroCodec

**Teaching machines to translate the language of data.**

NeuroCodec is an experimental neural data-translation system. Phase 1 tests whether parallel specialist networks can learn a shared latent representation of structured records and reconstruct the same information in a different encoding.

## Phase 1 research question

Can structure, semantic, and temporal specialist networks learn complementary representations that can be fused into a shared latent space and decoded into another structured format?

The first prototype supports JSON, CSV, and a compact custom pipe format.

## Architecture

```
Input record
    |
    +--> Structure specialist
    +--> Semantic specialist
    +--> Temporal specialist
    |
    v
Shared latent representation
    |
    v
Target decoder
    |
JSON / CSV / custom
```

The prototype deliberately separates **information representation** from **wire encoding**. It does not claim universal format translation yet; unseen-format generalization is a later experiment.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Run the demo:

```bash
python -m neurocodec.demo
```

Run the API:

```bash
uvicorn app.api.main:app --reload
```

Then open the interactive API documentation at `/docs`.

## Research roadmap

- [x] Parallel specialist model skeleton
- [x] Shared latent fusion
- [x] JSON / CSV / custom codec adapters
- [x] Reconstruction and round-trip validation
- [ ] Train on paired formats
- [ ] Hold out a target format during training
- [ ] Live stream translation
- [ ] Quantitative semantic/structural metrics
- [ ] Arc settlement layer for paid machine data transformation

## Status

Early research prototype. Results are experimental and should not be interpreted as evidence of universal data-format translation.
