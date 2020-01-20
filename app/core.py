'''Core operations module.

Includes functions for shortening and lengthening URLs, plus associated
helper functions.
'''


class InvalidURLError(Exception):
    '''Raised in certain situations when a string is not a valid URL.'''
    pass

class InvalidShortKeyError(Exception):
    '''Raised in certain situations when a string is not a valid short URL key.'''
    pass

class OutOfShortKeysError(Exception):
    '''Raised when there are no more available short URL keys.'''
    pass


def shorten_url(url: str) -> str:
    '''Shorten a URL.

    Given an arbitrarily long URL, convert it into a short URL, and
    insert this new (short,long) pair into the database. Return the key
    of the shortened URL. If the argument is not a valid URL, raise
    InvalidURLError, or if there are no more available short URL keys,
    raise OutOfShortKeysError. In both of these cases, the conversion is
    unsuccessful, and no database operations are performed.

    Args:
        url (str): The URL to be shortened

    Returns:
        str: The key of the shortened URL

    Raises:
        InvalidURLError: The input argument is not a valid URL
        OutOfShortKeysError: There are no more available short URL keys
    '''
    pass


def lengthen_url(key: str) -> str:
    '''Lengthen a URL.

    Given the key of a short URL, return the corresponding (long) URL.
    If the argument is an invalid short key, return InvalidShortKeyError.
    If the short key isn't associated with any URL, return None.

    Args:
        key (str): The short URL key to lookup

    Returns:
        str: The URL associated with the short key provided as an argument

    Raises:
        InvalidShortKeyError: The argument is not a valid short key
    '''
    pass


def _try_insert(key: str, url: str) -> bool:
    '''Try to insert a (key,url) pair into the database.

    Try to insert a (key,url) pair into the database, and return a bool
    indicating whether the pair exists in the database. True may be
    returned either because the pair was successfully inserted, or
    because it already existed in the database. Note that this function
    *does not* sanitize the input arguments; this is the responsibility of
    the caller.

    Args:
        key (str): a short URL key to be associated with the URL
        url (str): a URL to be associated with the short key

    Returns:
        bool: Whether the (key,url) pair provided as arguments exists in
              the database
    '''
    pass


def _key_from_hex(hexs: str) -> str:
    '''Derive a short URL key from a hexidecimal string.

    Given a string of hexadecimal characters, return a short URL key,
    which is deterministically derived from the argument. The argument
    string will be consumed as much as possible, so the length of the
    returned short key depends on the length of the argument string.
    Note that this function assumes that the argument passed in is a valid
    hexadecimal string; sanitation is the responsibility of the caller.

    Args:
        hexs (str): a string of hexidecimal characters

    Returns:
        str: a short URL key
    '''
    pass


def _next_key(key: str) -> str:
    '''Return the next greatest key.

    Given a short URL key, reeturn the next greatest key, assuming an
    alphanumeric sort order. If there is no next greatest key, (i.e. the
    input key was the highest in the sort order, namely "zzzzzzz"),
    return None. Note that this function *does not* santitize the input
    argument. A valid key is assumed to be provided, and sanitation is
    the responsibility of the caller.

    Args:
        key (str): A short URL key

    Returns:
        str: The next greatest short URL key
    '''
    pass


def _is_valid_url(url: str) -> bool:
    '''Return a boolean indicating whether the argument is a valid URL.'''
    pass


def _is_valid_key(key: str) -> bool:
    '''Return a boolean indicating whether the argument is a valid short URL key.'''
    pass
