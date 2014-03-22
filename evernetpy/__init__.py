import base64
import datetime
from execute import execute_listing_query, execute_photo_query
from lookups import look_up_all_fields

PROPERTY_TYPES = [
    'BUSO',
    'COMI',
    'COND',
    'FARM',
    'MANU',
    'MULT'
    'MULT',
    'RENT',
    'RESI',
    'TSHR',
    'VACL',
]


def get_all_listings(username, password, property_types=PROPERTY_TYPES):
    return get_new_listings(username, password, hours_previous=876581)


def get_all_active_mls_numbers(username, password, property_types=PROPERTY_TYPES):
    begin_date = "1990-01-01T00:00:00"
    end_date = "3000-01-01T00:00:00"

    for property_type in property_types:
        for row in execute_listing_query(username, password, 'RetrieveListingData', {'BeginDate': begin_date, 'EndDate': end_date, 'MLS': 'nwmls', 'PropertyType': property_type, 'Status': 'A'}, filter="LN,ST"):
            info = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            if info.get('ST') == 'A':
                yield info.get('LN')


def get_new_listings(username, password, hours_previous=24, property_types=PROPERTY_TYPES):
    begin_date = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours_previous)).strftime('%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    for property_type in property_types:
        for row in execute_listing_query(username, password, 'RetrieveListingData', {'BeginDate': begin_date, 'EndDate': end_date, 'MLS': 'nwmls', 'PropertyType': property_type}):
            out = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}', ''), c.text) for c in row.getchildren()])
            yield look_up_all_fields(username, password, out)


def get_photos(username, password, listing_id):
    for row in execute_photo_query(username, password, listing_id):
        out = dict([(c.tag.replace('{NWMLS:EverNet:ImageData:1.0}', ''), c.text) for c in row.getchildren()])
        out['BLOB'] = base64.b64decode(out['BLOB'])
        yield out
