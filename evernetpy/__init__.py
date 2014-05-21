import base64
import datetime
from execute import execute_listing_query, execute_photo_query
from lookups import look_up_all_fields
from criteria import iterate_criteria



def get_all_listings(username, password, property_types=[], areas=[], cities=[]):
    return get_new_listings(
        username,
        password,
        hours_previous=876581,
        property_types=property_types,
        areas=areas,
        cities=[]
    )


def get_all_active_mls_numbers(username, password, property_types=[], areas=[], cities=[]):
    for criteria in iterate_criteria('1990-01-01T00:00:00', '3000-01-01T00:00:00', status=['A'], property_types=property_types, areas=areas, cities=cities):
        for row in execute_listing_query(username, password, 'RetrieveListingData', criteria, filter="LN,ST"):
            info = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            yield info.get('LN')


def get_new_listings(username, password, hours_previous=24, property_types=[], areas=[], cities=[]):
    begin_date = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours_previous)).strftime('%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    for criteria in iterate_criteria(begin_date, end_date, property_types, areas, cities):
        for row in execute_listing_query(username, password, 'RetrieveListingData', criteria):
            out = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            yield look_up_all_fields(username, password, out)


def get_photos(username, password, listing_id):
    for row in execute_photo_query(username, password, listing_id):
        out = dict([(c.tag.replace('{NWMLS:EverNet:ImageData:1.0}', ''), c.text) for c in row.getchildren()])
        out['BLOB'] = base64.b64decode(out['BLOB'])
        yield out
