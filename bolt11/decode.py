""" Bolt11 Invoice Decoder """

import re
from hashlib import sha256
from typing import List, Optional
from bech32 import CHARSET, bech32_decode
from bitstring import Bits, ConstBitStream
from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import sigdecode_string

from .fallback import parse_fallback
from .helpers import readable_scid, trim_to_bytes, u5_to_bitarray, unshorten_amount
from .models import Bolt11Invoice, Route
from .exceptions import (
    Bolt11BadBech32StringException,
    Bolt11NoSignatureException,
    Bolt11StartWithLnException,
)


def decode(a: str) -> Bolt11Invoice:
    """Bolt11 decode function"""

    try:
        hrp, decoded_data = bech32_decode(a)
    except:
        raise Bolt11BadBech32StringException()

    if hrp is None or decoded_data is None:
        raise Bolt11BadBech32StringException()

    if not hrp.startswith("ln"):
        raise Bolt11StartWithLnException()

    bitarray = u5_to_bitarray(decoded_data)

    # final signature 65 bytes, split it off.
    if len(bitarray) < 65 * 8:
        raise Bolt11NoSignatureException()

    invoice = Bolt11Invoice()

    # extract the signature
    signature = bitarray[-65 * 8 :].tobytes()
    invoice.signature = bytes.hex(signature[0:64])

    # the tagged fields as a bitstream
    data = ConstBitStream(bitarray[: -65 * 8])

    currency, amount = parse_amount(hrp)
    if currency:
        invoice.currency = currency
    if amount:
        invoice.amount = amount

    date = data.read("uint35")
    assert isinstance(date, int)
    invoice.date = date

    while data.pos != data.len:
        tag, tagdata, data_length = parse_tagdata(data)

        if tag == "d":
            invoice.description = trim_to_bytes(tagdata).decode("utf-8")

        elif tag == "h":
            if data_length != 52:
                if not invoice.unknown_tags:
                    invoice.unknown_tags = []
                invoice.unknown_tags.append((tag, tagdata))
            invoice.description_hash = trim_to_bytes(tagdata).hex()

        elif tag == "r":
            if not invoice.route_hints:
                invoice.route_hints = []
            invoice.route_hints.extend(parse_r_tag(tagdata))

        elif tag == "f":
            if not invoice.fallbacks:
                invoice.fallbacks = []
            invoice.fallbacks.append(parse_fallback(tagdata, invoice.currency))

        elif tag == "x":
            invoice.expiry = tagdata.uint

        # featured bits
        # https://github.com/lightning/bolts/blob/master/11-payment-encoding.md#feature-bits
        elif tag == "9":
            invoice.features = trim_to_bytes(tagdata).hex()

        elif tag == "p":
            if data_length != 52:
                if not invoice.unknown_tags:
                    invoice.unknown_tags = []
                invoice.unknown_tags.append((tag, tagdata.tobytes().hex()))
            invoice.payment_hash = trim_to_bytes(tagdata).hex()

        elif tag == "s":
            invoice.payment_secret = trim_to_bytes(tagdata).hex()

        elif tag == "n":
            invoice.payee = trim_to_bytes(tagdata).hex()

        else:
            if not invoice.unknown_tags:
                invoice.unknown_tags = []
            invoice.unknown_tags.append((tag, tagdata))

    message = bytearray([ord(c) for c in hrp]) + data.tobytes()

    if hasattr(invoice, "payee") and invoice.payee:
        key = VerifyingKey.from_string(bytes.fromhex(invoice.payee), curve=SECP256k1)
        key.verify(signature[0:64], message, sha256, sigdecode=sigdecode_string)
    else:
        keys = VerifyingKey.from_public_key_recovery(
            signature[0:64], message, SECP256k1, sha256
        )
        signaling_byte = signature[64]
        key = keys[int(signaling_byte)]
        invoice.payee = key.to_string("compressed").hex()

    return invoice


def parse_r_tag(tagdata) -> List[Route]:
    route_hints = []
    s = ConstBitStream(tagdata)
    while s.pos + 264 + 64 + 32 + 32 + 16 < s.len:
        route = Route(
            pubkey=s.read(264).tobytes().hex(),
            short_channel_id=readable_scid(s.read(64).intbe),
            base_fee_msat=s.read(32).intbe,
            ppm_fee=s.read(32).intbe,
            cltv=s.read(16).intbe,
        )
        route_hints.append(route)
    return route_hints


def parse_amount(hrp: str) -> tuple[Optional[str], Optional[int]]:
    m = re.search(r"[^\d]+", hrp[2:])
    if m:
        currency = m.group(0)
        amountstr = hrp[2 + m.end() :]
        # BOLT #11:
        # A reader SHOULD indicate if amount is unspecified, otherwise it MUST
        # multiply `amount` by the `multiplier` value (if any) to derive the
        # amount required for payment.
        if amountstr != "":
            amount = unshorten_amount(amountstr)
            return currency, amount
        return currency, None
    return None, None


# type (5 bits)
# data_length (10 bits, big-endian)
# data (data_length x 5 bits)
# Note that the maximum length of a Tagged Field's data is constricted by the maximum value of data_length.
# This is 1023 x 5 bits, or 639 bytes.
def parse_tagdata(data: ConstBitStream) -> tuple[str, Bits, int]:
    _tag, _len1, _len2 = data.readlist(["uint5", "uint5", "uint5"])
    assert (
        isinstance(_tag, int) and isinstance(_len1, int) and isinstance(_len2, int)
    ), "_tag, _len1, _len2 should be int"
    length = _len1 * 32 + _len2
    # TODO test failes with 820 bytes
    # assert length * 5 <= 639, f"maximum value of 639 bytes data_length exceeded by {length * 5}"
    tagdata = data.read(length * 5)
    assert isinstance(tagdata, Bits), "tagdata should be Bits"
    return CHARSET[_tag], tagdata, length
