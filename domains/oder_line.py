from __future__ import annotations
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

