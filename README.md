# NeuroCodec

**Specification-conditioned neural translation with Arc Mainnet settlement.**

The web app runs the neural translation pipeline and uses **Arc Mainnet** for real USDC settlement.

- Network: **Arc Mainnet**
- Chain ID: **5042**
- RPC: `https://rpc.mainnet.arc.io`
- USDC: `0x3600000000000000000000000000000000000000`
- Gas asset: USDC
- Demo price: **0.01 USDC**

Arc Mainnet is live, and Arc Microgrants requires submitted projects to be deployed and working on Arc Mainnet.

### Payment + provenance

```
record + target specification
          |
          v
      NeuroCodec
          |
          v
 translation + SHA-256 receipt
          |
          v
 user signs 0.01 USDC native transfer
          |
          +--> receipt digest in transaction data
          |
          v
       Arc Mainnet
```

The dataset remains off-chain. The Arc transaction provides the payment and carries the receipt digest.

## Deployment

Set this Vercel environment variable:

```
ARC_RECIPIENT_ADDRESS=0xYOUR_ARC_MAINNET_WALLET
```

No private key is required. The user's connected wallet signs the payment.

The production app rejects Arc Testnet configuration and only accepts chain ID **5042**.

## Local development

```bash
pip install -r requirements.txt
pytest -q
python scripts/run_api.py
```

## Research boundary

NeuroCodec remains a research prototype and does not claim perfect zero-shot translation of every arbitrary binary format.

## License

See repository license.
