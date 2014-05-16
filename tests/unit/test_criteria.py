from evernetpy.criteria import iterate_criteria

def test_iterate_criteria_basic():
    output = [x for x in iterate_criteria('foo','bar')]
    print output
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar'}
    ]

def test_iterate_criteria_empty_areas():
    output = [x for x in iterate_criteria('foo','bar', property_types=[1,2,3])]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 2},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 3}
    ]

def test_iterate_criteria_property_types_and_areas():
    output = [x for x in iterate_criteria('foo','bar', property_types=[1,2], areas=[1,2])]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 1, 'EndDate': 'bar', 'Area': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 1, 'EndDate': 'bar', 'Area': 2},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 2, 'EndDate': 'bar', 'Area': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 2, 'EndDate': 'bar', 'Area': 2}
    ]

def test_iterate_criteria_property_types_and_areas_and_cities():
    output = [x for x in iterate_criteria('foo','bar', property_types=[1,2], areas=[1,2], cities=[1,2])]
    assert output == [
        {'City': 1, 'EndDate': 'bar', 'Area': 1, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 1},
        {'City': 2, 'EndDate': 'bar', 'Area': 1, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 1},
        {'City': 1, 'EndDate': 'bar', 'Area': 2, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 1},
        {'City': 2, 'EndDate': 'bar', 'Area': 2, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 1},
        {'City': 1, 'EndDate': 'bar', 'Area': 1, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 2},
        {'City': 2, 'EndDate': 'bar', 'Area': 1, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 2},
        {'City': 1, 'EndDate': 'bar', 'Area': 2, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 2},
        {'City': 2, 'EndDate': 'bar', 'Area': 2, 'BeginDate': 'foo', 'MLS': 'nwmls', 'PropertyType': 2}
    ]
