# NeuroCodec

**Specification-conditioned neural translation for structured data.**

NeuroCodec explores whether a shared neural representation can separate **what data means** from **how a target format represents it**.

## Core idea

Instead of building a separate translation model for every pair:

```
JSON -> CSV
JSON -> XML
CSV  -> PIPE
...
```

NeuroCodec represents the target format as a machine-readable specification:

```
data -> shared latent <- format specification
                         |
                         v
                  conditional decoder
```

The same pipeline can then adapt to a previously unregistered format specification.

## Current capabilities

- parallel neural data encoder
- learned format-specification encoder
- conditional decoder
- held-out format experiments
- bounded live-stream adaptation
- unregistered custom-format adaptation
- adversarial specification validation
- FastAPI demonstration API
- verifiable SHA-256 translation receipts
- Arc settlement intents without private-key custody

## Quick start

```bash
pip install -r requirements.txt
pytest -q
```

API:

```bash
pip install -r requirements-api.txt
python scripts/run_api.py
```

Final benchmark:

```bash
python scripts/run_final_benchmark.py
```

## Documentation

- `docs/architecture.md`
- `docs/experiments.md`
- `docs/demo.md`
- `docs/arc-settlement.md`
- `docs/submission.md`

## Scientific boundary

This project is a research prototype. It does not claim perfect zero-shot translation of every arbitrary binary format. Benchmark results should be generated from the supplied commands and reported with their limitations.

## License

See repository license.
