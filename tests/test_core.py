import pytest
from config import Config
from app import create_app, db, core


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


# @pytest.fixture
# def app():
#     app = create_app(TestConfig)
#     app_context = app.app_context()
#     app_context.push()
#     db.create_all()
#     yield app


def test__is_valid_url():
    assert core._is_valid_url('http://www.example.com/')
    assert core._is_valid_url('https://www.google.com/maps/place/Bow+Fire+Department/@43.159812,-71.5455405,15z/data=!4m5!3m4!1s0x89e24050a6762815:0x2e1f15765f6bc2cb!8m2!3d43.1568232!4d-71.5337983')
    assert core._is_valid_url('https://www.youtube.com/watch?v=0ROZRNZkPS8')
    assert core._is_valid_url('http://localhost:5000/')
    assert core._is_valid_url('ftp://my.ftp.site/test')

    # not a string
    assert not core._is_valid_url(3)
    # empty string
    assert not core._is_valid_url('')
    # nonsense
    assert not core._is_valid_url('sldkfjlsdkfjlsdkjf')
    # UTF-8 nonsense
    assert not core._is_valid_url('橦獬此橦獬此晪⤧⌦㜵㐳㬴')
    # invalid schema
    assert not core._is_valid_url('sqt://my.sqt/test')
    # missing forward slash
    assert not core._is_valid_url('http:/my.sqt/test')
    # nonsense after the schema
    assert not core._is_valid_url('http://a;lkdjlskdjflskdjflsdkjf')
    # missing suffix after period
    assert not core._is_valid_url('http://sldjflskdjf./')
    # missing prefix before period
    assert not core._is_valid_url('http://.ldkjf/')


def test__is_valid_key():
    assert core._is_valid_key('7OuG89h')
    assert core._is_valid_key('ZzZA001q')
    assert core._is_valid_key('2tzIJGEQm4')

    # not a string
    assert not core._is_valid_key(3)
    # empty string
    assert not core._is_valid_key('')
    # UTF-8 nonsense
    assert not core._is_valid_url('橦獬此橦獬此晪⤧⌦㜵㐳㬴')
    # invalid char
    assert not core._is_valid_key('t!IEQm4y')
    # invalid char
    assert not core._is_valid_key('t IEQm4y')
    # invalid char
    assert not core._is_valid_key('t-IEQm4y')
    # too long
    assert not core._is_valid_key('2tzIJGEQm4y')
    # too short
    assert not core._is_valid_key('2t3d0d')


def test__next_key__common():
    assert core._next_key('7OuG89h') == '7OuG89i'
    assert core._next_key('7OuG89H') == '7OuG89I'
    assert core._next_key('7OuG894') == '7OuG895'

def test__next_key__wraparound():
    assert core._next_key('7OuG899') == '7OuG89A'
    assert core._next_key('7OuG8MZ') == '7OuG8Ma'
    assert core._next_key('7OuG8Mz') == '7OuG8N0'
    assert core._next_key('7OuG9zz') == '7OuGA00'
    assert core._next_key('zzzzzzz') == None


def test__key_from_hex__common():
    k = core._key_from_hex('f0c740728f139362bbbe572391fa1bee03b6271e')
    assert core._is_valid_key(k)
    # we should get the same key if we do it again
    assert k == core._key_from_hex('f0c740728f139362bbbe572391fa1bee03b6271e')

def test__key_from_hex__fillvalue():
    # there's a case where the converted value of a sextet is greater than
    # 62, in which case the fill value is injected. Craft a custom input
    # such that the fill value is triggered for all sextets.
    k = core._key_from_hex('ffffffffffffffffffffffffffffffffffffffff')
    # TODO what should this output?
    assert True


def test__try_insert__common(db):
    assert core._try_insert('7OuG89A', 'http://www.example.com/')

def test__try_insert__preexisting_key(db):
    db.insert('7OuG89A', 'http://www.example.com/')
    assert core._try_insert('7OuG89A', 'http://www.example.com/')

def test__try_insert__key_taken(db):
    db.insert('7OuG89A', 'http://www.foobar.com/')
    assert not core._try_insert('7OuG89A', 'http://www.example.com/')


def test_shorten_url__common():
    k = core.shorten_url('http://www.example.com')
    assert core._is_valid_key(k)
    # should get the same thing if we do it again
    assert k == core.shorten_url('http://www.example.com')

def test_shorten_url__invalid_url():
    with pytest.raises(core.InvalidURLError):
        core.shorten_url('lssldkakdk')

def test_shorten_url__out_of_space():
    # TODO
    # core.shorten_url('http://www.example.com/')
    pass


def test_lengthen_url__common():
    db.insert('7OuG89A', 'http://www.example.com/')
    assert 'http://www.example.com/' == core.lengthen_url('7OuG89A')
    # we should get the same thing if we do it again
    assert 'http://www.example.com/' == core.lengthen_url('7OuG89A')

def test_lengthen_url__nonexistent_key():
    assert core.lengthen_url('78dkSf3') == None

def test_lengthen_url__invalid_key():
    with pytest.raises(core.InvalidShortKeyError):
        core.lengthen_url('aah!!!')
