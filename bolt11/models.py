import time
import json

from typing import List, NamedTuple, Optional
from secp256k1 import PublicKey


class Route(NamedTuple):
    pubkey: str
    short_channel_id: str
    base_fee_msat: int
    ppm_fee: int
    cltv: int


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, bytes):
        return obj.hex()
    if isinstance(obj, PublicKey):
        return obj.serialize().hex()
    if hasattr(obj, "__dict__"):
        return obj.__dict__


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

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        unknown_tags = (
            ", ".join([k + "=" + str(v) for k, v in self.unknown_tags])
            if self.unknown_tags
            else []
        )
        return f"LnAddr[{self.payee}, amount={self.amount}{self.currency} unknown_tags=[{unknown_tags}]]"
