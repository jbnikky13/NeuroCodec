from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import os
import re

ARC_MAINNET_CHAIN_ID = 5042
ARC_MAINNET_RPC = "https://rpc.mainnet.arc.io"
ARC_MAINNET_USDC = "0x3600000000000000000000000000000000000000"
ARC_NATIVE_DECIMALS = 18
ARC_USDC_DISPLAY_DECIMALS = 6
ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")


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


class ArcSettlement:
    def __init__(self, network: ArcNetwork | None = None):
        self.network = network or arc_network()

    def payment_intent(self, receipt, amount_usdc: str, recipient: str):
        try:
            amount = Decimal(str(amount_usdc))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount_usdc must be a valid decimal amount") from exc

        if amount <= 0:
            raise ValueError("amount_usdc must be positive")
        if amount.as_tuple().exponent < -ARC_NATIVE_DECIMALS:
            raise ValueError("amount_usdc has too many decimal places")
        if recipient and not ADDRESS_RE.fullmatch(recipient):
            raise ValueError("ARC_RECIPIENT_ADDRESS must be a valid EVM address")

        native_units = int(amount * (10 ** ARC_NATIVE_DECIMALS))

        return {
            "ready": bool(recipient),
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
