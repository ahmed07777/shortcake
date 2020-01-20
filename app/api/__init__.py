from flask import Blueprint
from . import routes

bp = Blueprint('api', __name__)
routes.register(bp)


def key_from_hex(hex_str: str) -> str:
    """Converts a hexadecimal string into a short url key.

    Given a string of hexidecimal characters, return a string that is suitable
    for use as a short url key. Short url keys consist of some number of letters
    (upper and lower case are distinct) and digits. This method will keep
    converting until it runs out of hexadecimal chars in the input parameter, so
    the length of the key returned depends on the length of the input.
    """
    pass
