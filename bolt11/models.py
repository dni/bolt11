import json
import time
from typing import List, NamedTuple, Optional


class Route(NamedTuple):
    pubkey: str
    short_channel_id: str
    base_fee_msat: int
    ppm_fee: int
    cltv: int


class Bolt11Invoice:
    payee: Optional[str] = None
    payment_hash: Optional[str] = None
    payment_secret: Optional[str] = None
    description: Optional[str] = None
    description_hash: Optional[str] = None
    signature: Optional[str] = None
    amount: Optional[int] = None
    route_hints: Optional[List] = None
    fallbacks: Optional[List] = None
    unknown_tags: Optional[List] = None
    date: int = int(time.time())
    features: Optional[str] = None
    currency: str = "bc"
    expiry: int = 1000

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__)
