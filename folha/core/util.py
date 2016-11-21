import os
from binascii import hexlify


def _createHash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5))