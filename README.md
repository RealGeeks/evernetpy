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

for listing in evernetpy.get_new_listings(username, password, hours_previous=24):
    print listing
```

## Get All Listings

Basically the same thing as get new listings, but returns all of them!

```python
import evernetpy

for listing in evernetpy.get_all_listings(username, password):
    print listing
```

## Get all Active Listings

```python
import evernetpy

for listing in evernetpy.get_all_listings(username, password, status=['A']):
    print listing
```

## Get only certain property types

All of get_new_listings, get_all_listings and get_all_active_mls_numbers take the optional argument property_types.
This should be an array of strings.  The available property types are as follows:

  * BUSO
  * COMI
  * COND
  * FARM
  * MANU
  * MUL
  * MULT
  * RENT
  * RESI
  * TSHR
  * VACL

By default, we will return all property types.

## Get only certain cities or areas

`get_new_listings`, `get_all_listings`, and `get_all_active_mls_numbers` take the optional arguments `areas` and `cities`.  They take an array of strings, and can be used to filter results by city or area.

## Get all active MLS numbers

```python
import evernetpy

evernetpy.get_all_active_mls_numbers(username, password)
```

This gives you an iterator with all the active MLS numbers in it.  You can also optionally pass the date_min and date_max fields.  They should be python datetime objects.

## Get a single property by mls_number

```python
import evernetpy

evernetpy.get_property(username, password, mls_number)
```

Returns a dictionary with the information from a single MLS number.  Looks up all the data for the lookup fields for you behind the scenes.

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

Just for kicks, here's how to turn on logging to the console for all loggers:

```python
console_log = logging.StreamHandler()
logging.getLogger().addHandler(console_log)
logging.getLogger().setLevel(logging.INFO)
```

# Changelog

* 2.3.0: You can now pass in date_min and date max to the `get_all_active_mls_nubmers` function
* 2.2.1: Bugfix: now you can actually use the status parameter to get all active listings
* 2.2.0: Add the ability to get all active listings
* 2.1.0: Add the ability to grab a single listing by MLS number
* 2.0.3: It turns out that Evernet assumes you only want 'RESI' properties if you don't explicitly specify, so let's do so.
* 2.0.2: Fixed a bug where items were not being filtered on in the `get_all_active_listings` method
* 2.0.1: Fixed a bug where status wasn't being filtered correctly
* 2.0.0: Add ability to filter by area and city, changed some method signatures so this is backwards-incompatible.
* 1.0.1: Fix bug where the new property types weren't getting passed along
* 1.0.0: Add support for different property types
* 0.1.0: Evernet changed their feed, it looks like "AR" is no longer a lookup field.
* 0.0.1: initial release

# License

The MIT License (MIT)

Copyright (c) 2014 Kevin McCarthy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
