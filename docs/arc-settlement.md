# Phase 9 — Arc settlement and verifiable receipts

A translation job now produces a receipt committing to its input, output, target specification and model version. The receipt has a SHA-256 digest.

The settlement boundary is:
translation -> receipt -> digest -> Arc payment intent -> external signer/wallet -> Arc transaction.

The implementation intentionally does not hold private keys or broadcast funds. Arc is the settlement layer; the neural model remains chain-independent.

Configure ARC_NETWORK, ARC_RPC_URL and ARC_CHAIN_ID when connecting a signer.
