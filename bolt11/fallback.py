import base58
from bech32 import bech32_encode

from .helpers import bitarray_to_u5

# Map of classical and witness address prefixes
base58_prefix_map = {"bc": (0, 5), "tb": (111, 196)}


def parse_fallback(fallback, currency) -> str:
    if currency == "bc" or currency == "tb":
        wver = fallback[0:5].uint
        if wver == 17:
            return base58.b58encode_check(bytes([base58_prefix_map[currency][0]])).hex()
        elif wver == 18:
            return base58.b58encode_check(
                bytes([base58_prefix_map[currency][1]]) + fallback[5:].tobytes()
            ).hex()
        elif wver <= 16:
            return bech32_encode(currency, bitarray_to_u5(fallback))
    return fallback.tobytes().hex()
