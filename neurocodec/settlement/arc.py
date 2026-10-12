from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json
import os
import re
from time import sleep
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ARC_MAINNET_CHAIN_ID = 5042
ARC_MAINNET_RPC = "https://rpc.mainnet.arc.io"
# Public Arc mainnet endpoints used only for read-only verification requests.
ARC_MAINNET_FALLBACK_RPCS = (
    "https://rpc.quicknode.mainnet.arc.io",
    "https://arc.drpc.org",
)
ARC_MAINNET_USDC = "0x3600000000000000000000000000000000000000"
ARC_NATIVE_DECIMALS = 18
ARC_USDC_DISPLAY_DECIMALS = 6
RPC_TIMEOUT_SECONDS = 5
RPC_ATTEMPTS = 2
ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
TX_HASH_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SIGNATURE_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ArcNetwork:
    name: str = "arc-mainnet"
    rpc_url: str = ARC_MAINNET_RPC
    chain_id: int = ARC_MAINNET_CHAIN_ID
    currency: str = "USDC"
    usdc_contract: str = ARC_MAINNET_USDC


def arc_network() -> ArcNetwork:
    requested_network = os.getenv("ARC_NETWORK", "arc-mainnet").strip().lower()
    try:
        requested_chain = int(os.getenv("ARC_CHAIN_ID", str(ARC_MAINNET_CHAIN_ID)))
    except ValueError as exc:
        raise RuntimeError("ARC_CHAIN_ID must be an integer") from exc

    if requested_network not in {"arc-mainnet", "arc"}:
        raise RuntimeError("NeuroCodec requires Arc Mainnet; testnet is disabled.")
    if requested_chain != ARC_MAINNET_CHAIN_ID:
        raise RuntimeError(
            f"NeuroCodec requires Arc Mainnet chain ID {ARC_MAINNET_CHAIN_ID}; received {requested_chain}."
        )

    rpc_url = os.getenv("ARC_RPC_URL", ARC_MAINNET_RPC).strip() or ARC_MAINNET_RPC
    if "testnet" in rpc_url.lower():
        raise RuntimeError("Arc Testnet RPCs are not allowed in the production app.")
    return ArcNetwork(rpc_url=rpc_url)


def _rpc_endpoints(primary_url: str) -> list[str]:
    """Return the configured primary followed by Arc mainnet read endpoints."""
    configured = os.getenv("ARC_RPC_FALLBACK_URLS")
    fallbacks = (
        [item.strip() for item in configured.split(",") if item.strip()]
        if configured is not None
        else list(ARC_MAINNET_FALLBACK_RPCS)
    )
    endpoints = []
    for url in [primary_url, *fallbacks]:
        if not url:
            continue
        if not url.lower().startswith("https://") or "testnet" in url.lower():
            raise RuntimeError("Arc RPC endpoints must use HTTPS and must not target testnet.")
        if url not in endpoints:
            endpoints.append(url)
    return endpoints


def _endpoint_label(url: str) -> str:
    """Expose the host in diagnostics without leaking path-based API keys."""
    return urlsplit(url).hostname or "configured RPC endpoint"


def _rpc_call(rpc_url: str, method: str, params: list):
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }).encode("utf-8")
    endpoints = _rpc_endpoints(rpc_url)
    failures = []

    # These are read-only JSON-RPC calls. Fail over between Arc Mainnet RPCs;
    # this function never submits or broadcasts a transaction.
    for endpoint in endpoints:
        for attempt in range(RPC_ATTEMPTS):
            request = Request(
                endpoint,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urlopen(request, timeout=RPC_TIMEOUT_SECONDS) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("RPC response was not a JSON object")
                if payload.get("error"):
                    error = payload["error"]
                    code = error.get("code") if isinstance(error, dict) else None
                    message = error.get("message") if isinstance(error, dict) else str(error)
                    raise ValueError(
                        f"JSON-RPC error code {code}: {message or 'unknown RPC error'}"
                    )
                if "result" not in payload:
                    raise ValueError("RPC response did not contain a result")
                result = payload["result"]
                if method == "eth_chainId":
                    try:
                        chain_id = int(result, 16) if isinstance(result, str) else int(result)
                    except (TypeError, ValueError):
                        raise ValueError("RPC returned an invalid chain ID")
                    if chain_id != ARC_MAINNET_CHAIN_ID:
                        raise ValueError(
                            f"endpoint reports chain ID {chain_id}, expected {ARC_MAINNET_CHAIN_ID}"
                        )
                return result
            except (URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
                failures.append(f"{_endpoint_label(endpoint)} attempt {attempt + 1}: {type(exc).__name__}: {exc}")
                if attempt + 1 < RPC_ATTEMPTS:
                    sleep(0.25)

    details = "; ".join(failures[-len(endpoints) * RPC_ATTEMPTS:])
    raise RuntimeError(
        f"Arc Mainnet RPC request '{method}' failed on {len(endpoints)} endpoint(s) "
        f"after up to {RPC_ATTEMPTS} attempt(s) each. Details: {details}. "
        "The transaction may still be successful; check Arc Explorer and retry verification "
        "with the same transaction hash. Do not submit another payment."
    )


class ArcSettlement:
    def __init__(self, network: ArcNetwork | None = None):
        self.network = network or arc_network()

    def payment_intent(self, receipt, amount_usdc: str, recipient: str):
        try:
            amount = Decimal(str(amount_usdc))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount_usdc must be a valid decimal amount") from exc

        if not amount.is_finite() or amount <= 0:
            raise ValueError("amount_usdc must be a finite positive amount")
        if amount.as_tuple().exponent < -ARC_NATIVE_DECIMALS:
            raise ValueError("amount_usdc has too many decimal places")
        if recipient and not ADDRESS_RE.fullmatch(recipient):
            raise ValueError("ARC_RECIPIENT_ADDRESS must be a valid EVM address")

        native_units = int(amount * (10 ** ARC_NATIVE_DECIMALS))
        if Decimal(native_units) != amount * (10 ** ARC_NATIVE_DECIMALS):
            raise ValueError("amount_usdc cannot be represented in native USDC units")

        return {
            "ready": bool(recipient and os.getenv("NEUROCODEC_RECEIPT_SECRET")),
            "network": "arc-mainnet",
            "chain_id": ARC_MAINNET_CHAIN_ID,
            "rpc_url": self.network.rpc_url,
            "asset": "USDC",
            "usdc_contract": ARC_MAINNET_USDC,
            "native_usdc_decimals": ARC_NATIVE_DECIMALS,
            "erc20_usdc_decimals": ARC_USDC_DISPLAY_DECIMALS,
            "amount": format(amount, "f"),
            "native_amount": str(native_units),
            "recipient": recipient,
            "receipt_digest": receipt.digest(),
            "purpose": "neurocodec-translation-job",
            "mainnet_only": True,
        }

    def verify_payment(
        self,
        tx_hash: str,
        receipt_digest: str,
        receipt_signature: str,
        recipient: str,
        amount_usdc: str = "0.01",
    ):
        if not TX_HASH_RE.fullmatch(tx_hash or ""):
            raise ValueError("transaction_hash must be a 32-byte hexadecimal transaction hash")
        if not DIGEST_RE.fullmatch(receipt_digest or ""):
            raise ValueError("receipt_digest must be a lowercase SHA-256 hex digest")
        if not SIGNATURE_RE.fullmatch(receipt_signature or ""):
            raise ValueError("receipt_signature must be a lowercase HMAC-SHA256 hex signature")
        if not ADDRESS_RE.fullmatch(recipient or ""):
            raise ValueError("Configured payment recipient is invalid")

        try:
            amount = Decimal(str(amount_usdc))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount_usdc must be a valid decimal amount") from exc
        if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -ARC_NATIVE_DECIMALS:
            raise ValueError("amount_usdc must be positive and have at most 18 decimal places")
        expected_value = int(amount * (10 ** ARC_NATIVE_DECIMALS))

        chain_id = _rpc_call(self.network.rpc_url, "eth_chainId", [])
        if not isinstance(chain_id, str) or int(chain_id, 16) != ARC_MAINNET_CHAIN_ID:
            raise RuntimeError("RPC endpoint is not reporting Arc Mainnet chain ID 5042.")

        tx = _rpc_call(self.network.rpc_url, "eth_getTransactionByHash", [tx_hash])
        if not tx:
            return {"verified": False, "status": "pending_or_not_found", "transaction_hash": tx_hash}

        if (tx.get("to") or "").lower() != recipient.lower():
            return {"verified": False, "status": "recipient_mismatch", "transaction_hash": tx_hash}
        if int(tx.get("value", "0x0"), 16) != expected_value:
            return {"verified": False, "status": "amount_mismatch", "transaction_hash": tx_hash}
        tx_chain_id = tx.get("chainId")
        if tx_chain_id is not None and int(tx_chain_id, 16) != ARC_MAINNET_CHAIN_ID:
            return {"verified": False, "status": "chain_mismatch", "transaction_hash": tx_hash}

        mined = _rpc_call(self.network.rpc_url, "eth_getTransactionReceipt", [tx_hash])
        if not mined:
            return {"verified": False, "status": "pending", "transaction_hash": tx_hash}
        if int(mined.get("status", "0x0"), 16) != 1:
            return {"verified": False, "status": "transaction_failed", "transaction_hash": tx_hash}
        if (mined.get("transactionHash") or "").lower() != tx_hash.lower():
            return {"verified": False, "status": "receipt_hash_mismatch", "transaction_hash": tx_hash}

        return {
            "verified": True,
            "status": "confirmed",
            "network": "arc-mainnet",
            "chain_id": ARC_MAINNET_CHAIN_ID,
            "transaction_hash": tx_hash,
            "recipient": recipient,
            "amount": format(amount, "f"),
            "receipt_digest": receipt_digest,
            "receipt_binding": "server-verified-signed-receipt; digest is submitted to the API and is not embedded in the transaction",
            "block_number": mined.get("blockNumber"),
        }
