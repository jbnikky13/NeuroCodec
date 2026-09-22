from __future__ import annotations
from dataclasses import dataclass
import os

ARC_MAINNET_CHAIN_ID = 5042
ARC_MAINNET_RPC = "https://rpc.mainnet.arc.io"
ARC_MAINNET_USDC = "0x3600000000000000000000000000000000000000"

@dataclass(frozen=True)
class ArcNetwork:
    name: str = "arc-mainnet"
    rpc_url: str = ARC_MAINNET_RPC
    chain_id: int = ARC_MAINNET_CHAIN_ID
    currency: str = "USDC"
    usdc_contract: str = ARC_MAINNET_USDC

def arc_network() -> ArcNetwork:
    requested_network = os.getenv("ARC_NETWORK", "arc-mainnet").strip().lower()
    requested_chain = int(os.getenv("ARC_CHAIN_ID", str(ARC_MAINNET_CHAIN_ID)))
    if requested_network not in {"arc-mainnet", "arc"}:
        raise RuntimeError("NeuroCodec requires Arc Mainnet; testnet is disabled.")
    if requested_chain != ARC_MAINNET_CHAIN_ID:
        raise RuntimeError(f"NeuroCodec requires Arc Mainnet chain ID {ARC_MAINNET_CHAIN_ID}; received {requested_chain}.")
    rpc_url = os.getenv("ARC_RPC_URL", ARC_MAINNET_RPC).strip() or ARC_MAINNET_RPC
    if "testnet" in rpc_url.lower():
        raise RuntimeError("Arc Testnet RPCs are not allowed in the production app.")
    return ArcNetwork(rpc_url=rpc_url)

class ArcSettlement:
    def __init__(self, network: ArcNetwork | None = None):
        self.network = network or arc_network()

    def payment_intent(self, receipt, amount_usdc, recipient):
        if not recipient:
            raise ValueError("ARC_RECIPIENT_ADDRESS is required")
        if float(amount_usdc) <= 0:
            raise ValueError("amount_usdc must be positive")
        return {
            "network": "arc-mainnet",
            "chain_id": ARC_MAINNET_CHAIN_ID,
            "rpc_url": self.network.rpc_url,
            "asset": "USDC",
            "usdc_contract": ARC_MAINNET_USDC,
            "native_usdc_decimals": 18,
            "erc20_usdc_decimals": 6,
            "amount": str(amount_usdc),
            "recipient": recipient,
            "receipt_digest": receipt.digest(),
            "purpose": "neurocodec-translation-job",
            "mainnet_only": True,
        }
