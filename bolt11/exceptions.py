class Bolt11SignatureRecoveryException(Exception):
    """Signature recovery failed"""


class Bolt11BadBech32StringException(Exception):
    """Bad Bech32 string Exception"""


class Bolt11NoSignatureException(Exception):
    """Too short to contain signature"""


class Bolt11StartWithLnException(Exception):
    """Does not start with ln"""


class Bolt11InvalidAmountException(Exception):
    """Invalid amount Exception"""
