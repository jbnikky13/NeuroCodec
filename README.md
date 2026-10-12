# NeuroCodec

**Specification-conditioned neural translation with Arc Mainnet settlement.**

The web app runs the neural translation pipeline and uses **Arc Mainnet** for real USDC settlement.

- Network: **Arc Mainnet**
- Chain ID: **5042**
- Primary RPC: `https://rpc.mainnet.arc.io`
- Read-only fallback RPCs: QuickNode and dRPC Arc Mainnet endpoints
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
          +--> signed receipt submitted to backend
          |
          v
       Arc Mainnet
```

The dataset and signed receipt remain off-chain. The Arc transaction provides the payment; the backend verifies the signed receipt separately because Arc rejects transaction data for this internal-account recipient type.

## Deployment

Set these Vercel environment variables:

```
ARC_RECIPIENT_ADDRESS=0xYOUR_ARC_MAINNET_WALLET
NEUROCODEC_RECEIPT_SECRET=<long-random-secret>
```

No private key is required. The user's connected wallet signs the payment. `NEUROCODEC_RECEIPT_SECRET` must be a long, randomly generated secret (keep it private and do not commit it). The API HMAC-signs receipt digests with this secret; payment verification rejects unsigned or invalidly signed receipts. Configure both environment variables in Vercel and redeploy.

Optional RPC configuration:

```
ARC_RPC_URL=https://rpc.mainnet.arc.io
ARC_RPC_FALLBACK_URLS=https://rpc.quicknode.mainnet.arc.io,https://arc.drpc.org
ARC_INFURA_API_KEY=your_infura_api_key
```

The fallback variable is a comma-separated list of trusted Arc Mainnet HTTPS JSON-RPC endpoints. If omitted, the app uses its built-in Arc Mainnet fallback endpoints. Arc RPC access may require a provider API key; configure an Arc-enabled Infura key as `ARC_INFURA_API_KEY` in Vercel to add the authenticated Infura Mainnet endpoint as a fallback. Create an API key at Infura and ensure Arc Mainnet is enabled for that key. Never put the key in source code or public logs. Never set RPCs to a testnet URL. Error messages log only the hostname, not the URL path.

The browser sends a standard native USDC transfer without transaction data. `/api/verify-payment` checks the HMAC signature of the submitted receipt, Arc Mainnet chain ID, transaction recipient, exact amount, and successful mined receipt. The receipt digest is not embedded on-chain; its association with the payment is asserted by the client and validated by the backend signature check. A transaction submission alone is not considered a verified payment. The `/formats` response distinguishes custom format support in the web API from codecs that are only registered in the research library.

### RPC recovery

Arc RPC reads retry transient failures and fail over to another Arc Mainnet endpoint. The chain-ID check rejects endpoints reporting a different chain and tries the next endpoint. If all endpoints fail, the error includes the failed endpoint host and failure category while omitting API-key paths.

If verification remains unavailable after a transaction has been submitted, the UI exposes **Verify existing transaction**. Enter the same transaction hash to retry verification; this action only calls the verification API and does not submit another payment. Always check Arc Explorer if the RPC is unavailable, and never pay a second time solely because verification timed out.

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
