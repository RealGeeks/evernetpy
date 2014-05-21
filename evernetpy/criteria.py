import itertools

def iterate_criteria(begin_date, end_date, property_types=None, areas=None, cities=None, status=None):
    base_criteria = {
        'MLS': 'nwmls',
        'BeginDate': begin_date,
        'EndDate': end_date,
    }
    if not cities and not areas and not property_types and not status:
        yield base_criteria
    else:
        areas = areas or [None]
        cities = cities or [None]
        property_types = property_types or [None]
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
