# NeuroCodec Architecture

Phase 1 has four layers:

1. **Codecs** convert JSON, CSV and the custom pipe representation to canonical records.
2. **Feature layer** creates a deterministic baseline vector.
3. **Parallel specialists** independently process structure, semantic and temporal signals.
4. **Fusion** combines the specialist outputs into a shared latent vector.

The current translator uses the canonical record as the reconstruction bridge. This establishes a measurable baseline before learned decoders are trained.

## Next experiment

Replace the deterministic feature baseline with trainable representation learning and add decoder heads trained on paired and held-out formats. The held-out-format test is designed to distinguish transferable representations from simple pair memorization.
