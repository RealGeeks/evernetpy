from evernetpy import get_new_listings, get_mls_numbers, get_photos, get_new_listings, get_property
from os import environ
import logging

username = environ.get('EVERNET_USERNAME')
password = environ.get('EVERNET_PASSWORD')

console_log = logging.StreamHandler()
logging.getLogger().addHandler(console_log)
logging.getLogger().setLevel(logging.INFO)

def test_get_new_sold_listings():
    results = get_new_listings(username, password, property_types=['RESI'])
    for r in results:
        if r['ST'].upper() == 'SOLD':
            assert 'SP' in r

def test_get_new_listings_unfiltered():
    results = get_new_listings(username, password)
    assert len([r for r in results])

def test_get_new_listings_filtered_by_area():
    results = get_new_listings(username, password, property_types=['RESI'], areas=['500'])
    areas = [r['AR'] for r in results]
    assert len(areas)
    assert all(['500 - East Side/South' in a for a in areas])

def test_get_new_listings_filtered_by_city():
    results = get_new_listings(username, password, property_types=['RESI'], cities=['Seattle'])
    cities = [r['CIT'] for r in results]
    assert len(cities)
    assert all([c == 'Seattle' for c in cities])

def test_get_all_active_mls_numbers():
    results = get_mls_numbers(username, password)
    assert len([r for r in results])

def test_get_photos():
    results = get_photos(username, password, 81796)
    assert len([r for r in results])

def test_get_property():
    property = get_property(username, password, '596799')
    # note: this must be an active mls number, if this test stats failing,
    # try changing it :)
    assert property
