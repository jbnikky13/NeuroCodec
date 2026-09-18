from __future__ import annotations
from dataclasses import dataclass
import os
@dataclass(frozen=True)
class ArcNetwork:
    name:str; rpc_url:str; chain_id:int|None; currency:str="USDC"
def arc_network():
    return ArcNetwork(os.getenv("ARC_NETWORK","arc-mainnet"),os.getenv("ARC_RPC_URL",""),int(os.getenv("ARC_CHAIN_ID","0")) or None)
class ArcSettlement:
    def __init__(self,network=None): self.network=network or arc_network()
    def payment_intent(self,receipt,amount_usdc,recipient):
        if not recipient: raise ValueError("recipient is required")
        if float(amount_usdc)<=0: raise ValueError("amount_usdc must be positive")
        return {"network":self.network.name,"rpc_url_configured":bool(self.network.rpc_url),"chain_id":self.network.chain_id,"asset":"USDC","amount":amount_usdc,"recipient":recipient,"receipt_digest":receipt.digest(),"purpose":"neurocodec-translation-job"}
