import base64
import datetime
from execute import execute_listing_query, execute_photo_query
from lookups import look_up_all_fields
from criteria import iterate_criteria



def get_all_listings(username, password, property_types=[], areas=[], cities=[], status=[]):
    return get_new_listings(
        username,
        password,
        hours_previous=876581,
        property_types=property_types,
        areas=areas,
        cities=cities,
        status=status,
    )


def get_all_active_mls_numbers(username, password, property_types=[], areas=[], cities=[], date_min=None, date_max=None):
    if not date_min:
        date_min = datetime.datetime(year=1990, month=1, day=1, hour=0, minute=0, second=0)
    if not date_max:
        date_max = datetime.datetime(year=3000, month=1, day=1, hour=0, minute=0, second=0)
    date_min = date_min.strftime('%Y-%m-%dT%H:%M:%S')
    date_max = date_max.strftime('%Y-%m-%dT%H:%M:%S')
    for criteria in iterate_criteria(date_min, date_max, status=['A'], property_types=property_types, areas=areas, cities=cities):
        for row in execute_listing_query(username, password, 'RetrieveListingData', criteria, filter="LN,ST"):
            info = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            yield info.get('LN')


def get_new_listings(username, password, hours_previous=24, property_types=[], areas=[], cities=[], status=[]):
    begin_date = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours_previous)).strftime('%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    for criteria in iterate_criteria(begin_date, end_date, property_types, areas, cities, status):
        for row in execute_listing_query(username, password, 'RetrieveListingData', criteria):
            out = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            yield look_up_all_fields(username, password, out)


def get_photos(username, password, listing_id):
    for row in execute_photo_query(username, password, listing_id):
        out = dict([(c.tag.replace('{NWMLS:EverNet:ImageData:1.0}', ''), c.text) for c in row.getchildren()])
        out['BLOB'] = base64.b64decode(out['BLOB'])
        yield out

def get_property(username, password, mls_number):
    criteria = {
        'MLS':'nwmls',
        'ListingNumber':mls_number
    }
    results = execute_listing_query(username, password, 'RetrieveListingData', criteria)
    first_result = next(results) # only return first match
    out = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in first_result.getchildren()])
    return look_up_all_fields(username, password, out)

