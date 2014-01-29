from execute import execute_listing_query

office_name_cache = {}
field_map_cache = {}

def look_up_office_name(username, password, office_id):
    if office_name_cache == {}:
        for r in execute_listing_query(username, password, 'RetrieveOfficeData', {'MLS':'nwmls'}):
            row = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/Standard/StandardXML1_1.xsd}',''),c.text) for c in r.getchildren()])
            office_name_cache[row.get('OfficeMLSID')] = row.get('OfficeName')
    return office_name_cache.get(office_id)

def get_lookup_table(username, password, prop_type, field_name):
    if len(field_map_cache.get(prop_type,{})) == 0:
        field_map_cache[prop_type] = {}
        for r in execute_listing_query(username, password, 'RetrieveAmenityData', {'MLS':'nwmls', 'PropertyType': prop_type}):
            field_name = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Code').text
            values = r.find('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Values').getchildren()
            row = dict([(c.tag.replace('{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}',''),c.text) for c in values])
            if field_name not in field_map_cache[prop_type]:
                field_map_cache[prop_type][field_name] = {}
            field_map_cache[prop_type][field_name][row['Code']] = row['Description']
    return field_map_cache[prop_type]

def look_up_all_fields(username, password, row):
    prop_type = row.get('PTYP')
    out = {}
    for key, value in row.iteritems():
        if not value:
            continue
        out[key] = []
        lookup_table = get_lookup_table(username, password, prop_type, key)
        if key not in lookup_table:
            out[key] = value
        else:
            for v in value.split('|'):
                out[key].append(lookup_table[key].get(v))
    return out

