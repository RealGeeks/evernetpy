from evernetpy import get_new_listings, get_all_active_mls_numbers, get_photos
from os import environ

username = environ.get('EVERNET_USERNAME')
password = environ.get('EVERNET_PASSWORD')

def test_get_new_listings():
    results = get_new_listings(username, password)
    assert len([r for r in results])

def test_get_all_active_mls_numbers():
    results = get_all_active_mls_numbers(username, password)
    assert len([r for r in results])

def test_get_photos():
    results = get_photos(username, password, 81796)
    assert len([r for r in results])
