from xml.etree.ElementTree import iterparse

SCHEMA_1_2_TYPES = [
    'BusinessOpportunity',
    'CommercialIndustrial',
    'FarmRanch',
    'Manufactured',
    'MultiFamily',
    'TimeShare',
    'VacantLand',
    'Condominium',
    'Residential',
]


TAGS_I_CARE_ABOUT = [
    '{http://www.nwmls.com/Schemas/General/EverNetAmenityXML.xsd}Amenity',
    '{http://www.nwmls.com/Schemas/General/EverNetOfficeXML.xsd}office',
    '{NWMLS:EverNet:ImageData:1.0}Image',
] + ['{http://www.nwmls.com/Schemas/Standard/StandardXML1_2.xsd}' + t for t in SCHEMA_1_2_TYPES]


def parse(data):
    for event, elem in iterparse(data):
        if elem.tag in TAGS_I_CARE_ABOUT:
            yield elem
            elem.clear()
