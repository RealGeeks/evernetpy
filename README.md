#evernetpy

Find yourself in the situation of having to work with the crazy NWMLS EverNet servers?  I know how you feel!

This library wraps all the terrible things you have to do to get data out of NWMLS and Evernet.

## Get New Listings

Use the `get_new_listings` method with your username and password.  This returns an iterator, each item in the iterator is a python dictionary with the listing data in it.  All the lookup fields have already been looked up for you.

```python
import evernetpy

for listing in evernetpy.get_new_listings(username, password):
    print listing
```

## Get All Listings

Basically the same thing as get new listings, but returns all of them!

```python
import evernetpy

for listing in evernetpy.get_new_listings(username, password):
    print listing
```

## Get all active MLS numbers

```python
import evernetpy

evernetpy.get_all_active_mls_numbers(username, password)
```

This gives you an iterator with all the active MLS numbers in it.

## Get Photos

Call this with the listing ID and you get an iterator with photos in it.  Each photo is a dictionary with some metadata about the photo.  The BLOB key has the binary of the actual photo.

```python
import evernetpy

evernetpy.get_photos(username, password, listing_id)
```

# Running tests
If you want to run the integration tests, you'll need an EverNet username and password.  Set the following environment variables before running the tests:

 * EVERNET_USERNAME
 * EVERNET_PASSWORD

# Debugging
Configure the python logger to barf out DEBUG if you want the HTTP going over the wire, INFO if you just want more stuff about the queries being run




