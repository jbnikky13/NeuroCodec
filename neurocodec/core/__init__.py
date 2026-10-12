"""Core utilities with lazy access to the optional research model."""

__all__ = ["record_to_features", "NeuroTranslator"]


def __getattr__(name: str):
    if name == "record_to_features":
        from .features import record_to_features

        return record_to_features
    if name == "NeuroTranslator":
        from .translator import NeuroTranslator

        return NeuroTranslator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
