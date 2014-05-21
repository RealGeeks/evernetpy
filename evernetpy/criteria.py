import itertools

ALL_PROPERTY_TYPES = [
    "BUSO",
    "COMI",
    "COND",
    "FARM",
    "MANU",
    "MULT",
    "RENT",
    "RESI",
    "TSHR",
    "VACL",
]


def iterate_criteria(begin_date, end_date, property_types=None, areas=None, cities=None, status=None):
    """
    NOTE: If you don't pass criteria to Evernet, it will assume you only want residential properties.
    That's why I will iterate through all availabe types unless you pass me a list of types you want
    explicitly.
    """
    base_criteria = {
        'MLS': 'nwmls',
        'BeginDate': begin_date,
        'EndDate': end_date,
    }
    areas = areas or [None]
    cities = cities or [None]
    property_types = property_types or ALL_PROPERTY_TYPES
    status = status or [None]
    for property_type, area, city, status in itertools.product(property_types, areas, cities, status):
        criteria = {}
        if area:
            criteria['Area'] = area
        if city:
            criteria['City'] = city
        if status:
            criteria['Status'] = status
        if property_type:
            criteria['PropertyType'] = property_type
        criteria.update(base_criteria)
        yield criteria
