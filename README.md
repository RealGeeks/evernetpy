#evernetpy

Have you found yourself in the situation of having to work with the crazy NWMLS EverNet data feed?  What is SOAP?  Didn't XML die in the 90s?  I know how you feel!

This library wraps all the terrible things you have to do to get data out of NWMLS and Evernet.

The listings returned by evernetpy are actually combined from several different tables in Evernet: The Listings table, the Amenities table, and the Offices table.  The amenities and office name are looked up and combined into the same result dictionary automatically.

## Installation

```bash
pip install evernetpy
```

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

# License

The MIT License (MIT)

Copyright (c) 2014 Kevin McCarthy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
