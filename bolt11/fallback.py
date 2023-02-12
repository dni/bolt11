""" Bolt11 fallbacks for decoder and encoder"""

import base58
from bech32 import bech32_decode, bech32_encode
from bitstring import pack

from .helpers import bitarray_to_u5, tagged, u5_to_bitarray

# Map of classical and witness address prefixes
base58_prefix_map = {"bc": (0, 5), "tb": (111, 196)}


def is_p2pkh(currency, prefix):
    return prefix == base58_prefix_map[currency][0]


def is_p2sh(currency, prefix):
    return prefix == base58_prefix_map[currency][1]


def parse_fallback(fallback, currency) -> str:
    """parse fallback addresses."""
    if currency in ("bc", "tb"):
        wver = fallback[0:5].uint
        if wver == 17:
            return base58.b58encode_check(bytes([base58_prefix_map[currency][0]])).hex()
        if wver == 18:
            return base58.b58encode_check(
                bytes([base58_prefix_map[currency][1]]) + fallback[5:].tobytes()
            ).hex()
        if wver <= 16:
            return bech32_encode(currency, bitarray_to_u5(fallback))
    return fallback.tobytes().hex()


def encode_fallback(fallback, currency):
    """Encode all supported fallback addresses."""
    if currency in ("bc", "tb"):
        fbhrp, witness = bech32_decode(fallback)
        if fbhrp:
            if fbhrp != currency:
                raise ValueError("Not a bech32 address for this currency")
            assert witness, "encode_fallback, witness is None"
            wver = witness[0]
            if wver > 16:
                raise ValueError(f"Invalid witness version {witness[0]}")
            wprog = u5_to_bitarray(witness[1:])
        else:
            addr = base58.b58decode_check(fallback)
            if is_p2pkh(currency, addr[0]):
                wver = 17
            elif is_p2sh(currency, addr[0]):
                wver = 18
            else:
                raise ValueError(f"Unknown address type for {currency}")
            wprog = addr[1:]
        return tagged("f", pack("uint:5", wver) + wprog)

    raise NotImplementedError(f"Support for currency {currency} not implemented")
