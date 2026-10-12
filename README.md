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
NEUROCODEC_RECEIPT_SECRET=<long-random-secret>
```

No private key is required. The user's connected wallet signs the payment. `NEUROCODEC_RECEIPT_SECRET` must be a long, randomly generated secret (keep it private and do not commit it). The API HMAC-signs receipt digests with this secret; payment verification rejects unsigned or invalidly signed receipts. Configure both environment variables in Vercel and redeploy.

The browser sends a native USDC transfer with `neurocodec:<receipt-digest>:<signature>` in transaction data. `/api/verify-payment` checks the signature, Arc Mainnet chain ID, transaction recipient, exact amount, transaction data, and successful mined receipt. A transaction submission alone is not considered a verified payment. The `/formats` response now distinguishes custom format support in the web API from codecs that are only registered in the research library.

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
