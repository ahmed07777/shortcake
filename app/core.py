'''Core operations module.

Includes functions for shortening and lengthening URLs, plus associated
helper functions.
'''

import re
import string
import hashlib
import itertools as it

from werkzeug.urls import url_parse, url_fix

from app.models import ShortURL
from app.db import db


SHORTKEY_LENGTH = 7  # can be increased up to 10 if need be
SHORTKEY_CHARSET = string.digits + string.ascii_uppercase + string.ascii_lowercase
N_SHORTKEY_CHARS = len(SHORTKEY_CHARSET)


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

    # The algorithm for converting a URL into a shortkey is as follows:
    #    1. Hash the URL and convert the hash into a string of characters from
    #       SHORTKEY_CHARSET
    #    2. Try the beginning of this string as a shortkey. If the key is taken,
    #       slide the shortkey "window" over by 1 and try again. Repeat this
    #       until the end of the string is reached.
    #    3. Take the current candidate key and increment it by 1 until an
    #       available shortkey is found
    #
    # The performance of this algorithm in the worst case is terrible, but per
    # the current parameters there are 7**62 possible shortkeys, so it is
    # unlikely that step 3 of the algorithms will ever be reached.

    # InvalidURLError is propogated to caller
    url = _validate_url(url)
    hashstr = hashlib.sha1(url.encode()).hexdigest()
    long_keystr = _key_from_hex(hashstr)
    for i in range(len(long_keystr) - SHORTKEY_LENGTH + 1):
        candidate_key = long_keystr[i:i+SHORTKEY_LENGTH]
        if _try_insert(candidate_key, url):
            return candidate_key
    # none of the key windows were available, so increment the current candidate
    # key until we find an available one
    initial_key = candidate_key
    cur = _next_key(initial_key)
    while cur != initial_key:
        if _try_insert(cur, url):
            return cur
        cur = _next_key(cur)
        if not cur:  # wrap around
            cur = '0' * SHORTKEY_LENGTH
    # there are no more available shortkeys
    raise OutOfShortKeysError


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
    if not _is_valid_key(key):
        raise InvalidShortKeyError
    existing_entry = ShortURL.query.get(key)
    if existing_entry:
        return existing_entry.url
    # key isn't in database
    return None


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
    existing_entry = ShortURL.query.filter_by(key=key).first()
    if existing_entry:
        return existing_entry.url == url
    db.session.add(ShortURL(key=key, url=url))
    db.session.commit()
    return True


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

    # from https://docs.python.org/3/library/itertools.html#itertools-recipes
    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return it.zip_longest(*args, fillvalue=fillvalue)

    hash_bytes = bytes.fromhex(hexs)
    # TODO is there a more efficient way to do this with bitmask operations?
    hash_binstr = ''.join(bin(b)[2:] for b in hash_bytes)
    keystr = ''
    shortkey_fillchar = None
    # NOTE 6 is hardcoded here because it is currently the smallest n for which
    # 2**n >= N_SHORTKEY_CHARS. If the shortkey charset were to change, this
    # number might need to be updated.
    for group in grouper(hash_binstr, 6, fillvalue='0'):
        sextet = ''.join(group)
        i = int(sextet, 2)
        # TODO are there *deterministic* ways of handling this edge case that
        # give more even distributions of shortkeys?
        if i >= N_SHORTKEY_CHARS:
            # compute shortkey_fillchar if we haven't already
            if not shortkey_fillchar:
                shortkey_fillchar = int(hash_binstr, 2) % N_SHORTKEY_CHARS
            i = shortkey_fillchar
        char = SHORTKEY_CHARSET[i]
        keystr += char
    return keystr


def _next_key(key: str) -> str:
    '''Return the next greatest key.

    Given a short URL key, return the next greatest key, assuming an
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
    ret = key
    for i in reversed(range(len(key))):
        k = key[i]
        if k == 'z':
            ret = ret[:i] + '0' + ret[i+1:]
        else:
            idx = SHORTKEY_CHARSET.find(k)
            ret = ret[:i] + SHORTKEY_CHARSET[idx+1] + ret[i+1:]
            break
    else:
        # we got the string 'zzzzzzz'
        return None
    return ret


def _validate_url(url: str) -> str:
    '''Validate a URL.

    Given a string, return a sanitized URL, or raise InvalidURLError if
    the string is not a valid URL.

    Args:
        url (str): The string to validate as a URL

    Returns:
        str: The sanitized, validated URL

    Raises:
        InvalidURLError: The argument is not a valid URL
    '''
    if not url or not isinstance(url, str): raise InvalidURLError
    # KISS. Can be expanded later if desired.
    valid_schemes = ['http', 'https']
    valid_netloc_pattern = re.compile(r'\w+\.\w+')

    url_tuple = url_parse(url, scheme='http')
    scheme, netloc, path = url_tuple.scheme, url_tuple.netloc, url_tuple.path
    if scheme not in valid_schemes: raise InvalidURLError
    if not re.match(valid_netloc_pattern, netloc) and \
       (netloc or not re.match(valid_netloc_pattern, path)):
        raise InvalidURLError
    return url_fix(url)


# TODO: I think the interface of this function should be changed to match
# that of _validate_url
def _is_valid_key(key: str) -> bool:
    '''Return a boolean indicating whether the argument is a valid short URL key.'''
    if not key or not isinstance(key, str): return False
    return all(c in SHORTKEY_CHARSET for c in key) and 7 <= len(key) <= 10
