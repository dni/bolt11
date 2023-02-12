import re
from typing import List

from bech32 import CHARSET
from bitstring import BitArray, ConstBitStream, pack

from .exceptions import Bolt11InvalidAmountException


# BOLT #11:
#
# A writer MUST encode `amount` as a positive decimal integer with no
# leading zeroes, SHOULD use the shortest representation possible.
def shorten_amount(amount) -> str:
    """Given an amount in bitcoin, shorten it"""
    # Convert to pico initially
    amount = int(amount * 10**12)
    units = ["p", "n", "u", "m", ""]
    unit = ""
    for unit in units:
        if amount % 1000 == 0:
            amount //= 1000
        else:
            break
    return str(amount) + unit


def unshorten_amount(amount: str) -> int:
    """Given a shortened amount, return millisatoshis"""
    # BOLT #11:
    # The following `multiplier` letters are defined:
    #
    # * `m` (milli): multiply by 0.001
    # * `u` (micro): multiply by 0.000001
    # * `n` (nano): multiply by 0.000000001
    # * `p` (pico): multiply by 0.000000000001
    units = {"p": 10**12, "n": 10**9, "u": 10**6, "m": 10**3}
    unit = str(amount)[-1]

    # BOLT #11:
    # A reader SHOULD fail if `amount` contains a non-digit, or is followed by
    # anything except a `multiplier` in the table above.
    if not re.fullmatch(r"\d+[pnum]?", str(amount)):
        raise Bolt11InvalidAmountException(f"Invalid amount '{amount}'")

    if unit in units:
        return int(int(amount[:-1]) * 100_000_000_000 / units[unit])
    else:
        return int(amount) * 100_000_000_000


# Tagged field containing BitArray
def tagged(char, l):
    # Tagged fields need to be zero-padded to 5 bits.
    while l.len % 5 != 0:
        l.append("0b0")
    return (
        pack(
            "uint:5, uint:5, uint:5",
            CHARSET.find(char),
            (l.len / 5) / 32,
            (l.len / 5) % 32,
        )
        + l
    )


def tagged_bytes(char, l):
    return tagged(char, BitArray(l))


def trim_to_bytes(barr):
    # removes a byte if necessary.
    b = barr.tobytes()
    if barr.len % 8 != 0:
        return b[:-1]
    return b


def readable_scid(short_channel_id: int) -> str:
    blockheight = (short_channel_id >> 40) & 0xFFFFFF
    transactionindex = (short_channel_id >> 16) & 0xFFFFFF
    outputindex = short_channel_id & 0xFFFF
    return f"{blockheight}x{transactionindex}x{outputindex}"


def u5_to_bitarray(arr: List[int]) -> BitArray:
    ret = BitArray()
    for a in arr:
        ret += pack("uint5", a)
    return ret


def bitarray_to_u5(barr):
    assert barr.len % 5 == 0
    ret = []
    s = ConstBitStream(barr)
    while s.pos != s.len:
        ret.append(s.read("uint5"))
    return ret
