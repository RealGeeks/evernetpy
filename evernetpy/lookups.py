from execute import execute_listing_query
from collections import defaultdict
from memoize import memoize

office_name_cache = {}

FIXED_NWMLS_LOOKUPS = {
    'STA': {
        'A': 'Active',
        'CT': 'Contingent',
        'PB': 'Pending BU Requested',
        'PF': 'Pending Feasability',
        'PI': 'Pending Inspection',
        'PS': 'Pending Short Sale',
        'P': 'Pending',
        'E': 'Expired',
        'T': 'Temp. Off Markt.',
        'SFR': 'Sale Fail Release',
        'CA': 'Cancelled',
        'R': 'Rented',
        'S': 'Sold',
    }
}

def _get_offices(username, password):
    for row in execute_listing_query(username, password, 'RetrieveOfficeData', {'MLS': 'nwmls'}):
        row = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_1.xsd}', ''), c.text) for c in r.getchildren()])
        yield row


def look_up_office_name(offices, office_id):
    if office_name_cache == {}:
        for office in offices:
            office_name_cache[office.get('OfficeMLSID')] = office.get('OfficeName')
    return office_name_cache.get(office_id)


@memoize
def _get_amenities(username, password, prop_type):
    for r in execute_listing_query(username, password, 'RetrieveAmenityData', {'MLS': 'nwmls', 'PropertyType': prop_type}):
        field_name = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Code').text
        values = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Values').getchildren()
        row = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}', ''), c.text) for c in values])
        yield field_name, row


def get_amenities_table(amenities):
    field_map = defaultdict(dict)
    for field_name, row in amenities:
        field_map[field_name][row['Code']] = row['Description']
    return field_map



def look_up_all_fields(username, password, row):
    prop_type = row.get('PTYP')
    out = {}
    for key, value in row.iteritems():
        if not value:
            continue
        out[key] = []
        lookup_table = get_amenities_table(_get_amenities(username, password, prop_type))
        if key not in lookup_table:
            out[key] = value
        else:
            for v in value.split('|'):
                out[key].append(lookup_table[key].get(v))
    return out
