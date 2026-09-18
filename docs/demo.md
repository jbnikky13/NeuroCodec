# Phase 8 — API and interactive demo

Start the API:

```bash
pip install -r requirements-api.txt
python scripts/run_api.py
```

Open `demo/index.html` through the same host/proxy or use the API directly.

Endpoints:
- `GET /health`
- `GET /formats`
- `GET /demo/sample`
- `POST /translate`

The demo intentionally exposes the custom specification. This makes the core research idea visible: the target format is described rather than selected from a fixed list.

Phase 8 is a presentation/API layer; it does not change the scientific claims established by Phases 1–7.
