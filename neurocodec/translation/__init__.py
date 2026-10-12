"""Translation modules with optional heavy research dependencies.

The production API uses lightweight deterministic adapters and must be importable
without PyTorch. Load the research-only LearnedTranslator lazily when requested.
"""

__all__ = ["LearnedTranslator"]


def __getattr__(name: str):
    if name == "LearnedTranslator":
        from .learned import LearnedTranslator

        return LearnedTranslator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
