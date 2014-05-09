from evernetpy import _get_criteria

def test_get_criteria_empty():
    output = [x for x in _get_criteria('foo','bar', [], [])]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar'},
    ]

def test_get_criteria_empty_areas():
    output = [x for x in _get_criteria('foo','bar', [1,2,3], None)]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 2},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'PropertyType': 3}
    ]

def test_get_criteria_empty_property_types():
    output = [x for x in _get_criteria('foo','bar', None, [1,2,3])]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'Area': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'Area': 2},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'EndDate': 'bar', 'Area': 3}
    ]

def test_get_criteria_property_types_and_areas():
    output = [x for x in _get_criteria('foo','bar', [1,2], [1,2])]
    assert output == [
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 1, 'EndDate': 'bar', 'Area': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 1, 'EndDate': 'bar', 'Area': 2},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 2, 'EndDate': 'bar', 'Area': 1},
        {'MLS': 'nwmls', 'BeginDate': 'foo', 'PropertyType': 2, 'EndDate': 'bar', 'Area': 2}
    ]
