from .core.translator import NeuroTranslator


def main() -> None:
    translator = NeuroTranslator()
    sample = "temperature=28.4|location=PH|timestamp=1758211200|status=OK"
    result = translator.translate(sample, "pipe", "json")
    print("NeuroCodec Phase 1 demo")
    print("Input:", sample)
    print("Output:", result["output"])
    print("Latent dimensions:", len(result["latent"]))


if __name__ == "__main__":
    main()
