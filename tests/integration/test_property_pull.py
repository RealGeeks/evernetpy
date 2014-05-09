from evernetpy import get_new_listings, get_all_active_mls_numbers, get_photos, get_new_listings
from os import environ

username = environ.get('EVERNET_USERNAME')
password = environ.get('EVERNET_PASSWORD')

def test_get_new_listings_unfiltered():
    results = get_new_listings(username, password)
    assert len([r for r in results])

def test_get_new_listings_filtered_by_area():
    results = get_new_listings(username, password, property_types=['RESI'], areas=['500'])
    import pdb;pdb.set_trace()
    cities = [r['AR'] for r in results]
    assert len(cities)
    assert all([c == 'Seattle' for c in cities])

def test_get_all_active_mls_numbers():
    results = get_all_active_mls_numbers(username, password)
    assert len([r for r in results])

def test_get_photos():
    results = get_photos(username, password, 81796)
    assert len([r for r in results])
