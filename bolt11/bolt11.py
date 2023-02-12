import hashlib
import re
from decimal import Decimal

from .models import Invoice, LnAddr, Route
from .helpers import (
    shorten_amount,
    unshorten_amount,
    u5_to_bitarray,
    bitarray_to_u5,
    trim_to_bytes,
    readable_scid,
    tagged_bytes,
)

from bitstring import pack, BitArray, ConstBitStream

from secp256k1 import PublicKey

from bech32 import bech32_decode, bech32_encode, CHARSET

from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import sigdecode_string


# def encode(options):
#     """Convert options into LnAddr and pass it to the encoder"""
#     addr = LnAddr()
#     addr.currency = options["currency"]
#     addr.fallback = options["fallback"] if options["fallback"] else None
#     if options["amount"]:
#         addr.amount = options["amount"]
#     if options["timestamp"]:
#         addr.date = int(options["timestamp"])

#     addr.paymenthash = bytes.fromhex(options["paymenthash"])

#     if options["description"]:
#         addr.tags.append(("d", options["description"]))
#     if options["description_hash"]:
#         addr.tags.append(("h", options["description_hash"]))
#     if options["expires"]:
#         addr.tags.append(("x", options["expires"]))

#     if options["fallback"]:
#         addr.tags.append(("f", options["fallback"]))
#     if options["route"]:
#         for r in options["route"]:
#             splits = r.split("/")
#             route = []
#             while len(splits) >= 5:
#                 route.append(
#                     (
#                         bytes.fromhex(splits[0]),
#                         bytes.fromhex(splits[1]),
#                         int(splits[2]),
#                         int(splits[3]),
#                         int(splits[4]),
#                     )
#                 )
#                 splits = splits[5:]
#             assert len(splits) == 0
#             addr.tags.append(("r", route))
#     return lnencode(addr, options["privkey"])


def lnencode(addr, privkey):
    if addr.amount:
        amount = Decimal(str(addr.amount))
        # We can only send down to millisatoshi.
        if amount * 10**12 % 10:
            raise ValueError(f"Cannot encode {addr.amount}: too many decimal places")

        amount = addr.currency + shorten_amount(amount)
    else:
        amount = addr.currency if addr.currency else ""

    hrp = "ln" + amount + "0n"

    # Start with the timestamp
    data = pack("uint:35", addr.date)

    # Payment hash
    data += tagged_bytes("p", addr.paymenthash)
    tags_set = set()

    for k, v in addr.tags:
        # BOLT #11:
        #
        # A writer MUST NOT include more than one `d`, `h`, `n` or `x` fields,
        if k in ("d", "h", "n", "x"):
            if k in tags_set:
                raise ValueError(f"Duplicate '{k}' tag")

        if k == "r":
            route = BitArray()
            for step in v:
                pubkey, channel, feebase, feerate, cltv = step
                route.append(
                    BitArray(pubkey)
                    + BitArray(channel)
                    + pack("intbe:32", feebase)
                    + pack("intbe:32", feerate)
                    + pack("intbe:16", cltv)
                )
            data += tagged("r", route)
        elif k == "f":
            data += encode_fallback(v, addr.currency)
        elif k == "d":
            data += tagged_bytes("d", v.encode())
        elif k == "x":
            # Get minimal length by trimming leading 5 bits at a time.
            expirybits = pack("intbe:64", v)[4:64]
            while expirybits.startswith("0b00000"):
                expirybits = expirybits[5:]
            data += tagged("x", expirybits)
        elif k == "h":
            data += tagged_bytes("h", v)
        elif k == "n":
            data += tagged_bytes("n", v)
        else:
            # FIXME: Support unknown tags?
            raise ValueError(f"Unknown tag {k}")

        tags_set.add(k)

    # BOLT #11:
    #
    # A writer MUST include either a `d` or `h` field, and MUST NOT include
    # both.
    if "d" in tags_set and "h" in tags_set:
        raise ValueError("Cannot include both 'd' and 'h'")
    if "d" not in tags_set and "h" not in tags_set:
        raise ValueError("Must include either 'd' or 'h'")

    # We actually sign the hrp, then data (padded to 8 bits with zeroes).
    privkey = secp256k1.PrivateKey(bytes.fromhex(privkey))
    sig = privkey.ecdsa_sign_recoverable(
        bytearray([ord(c) for c in hrp]) + data.tobytes()
    )
    # This doesn't actually serialize, but returns a pair of values :(
    sig, recid = privkey.ecdsa_recoverable_serialize(sig)
    data += bytes(sig) + bytes([recid])

    return bech32_encode(hrp, bitarray_to_u5(data))
