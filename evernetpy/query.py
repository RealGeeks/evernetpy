VALID_LISTING_QUERY_FIELDS = [
    'MLS',
    'ListingNumber',
    'PropertyType',
    'Status',
    'County',
    'Area',
    'City',
    'BeginDate',
    'EndDate',
    'OfficeId',
    'AgentId',
    'Bedrooms',
    'Bathrooms',
]


PHOTO_QUERY = '<ImageQuery xmlns="NWMLS:EverNet:ImageQuery:1.0"><Auth><UserId>{UserId}</UserId><Password>{Password}</Password></Auth><Query><ByListingNumber>{ListingNumber}</ByListingNumber></Query><Results><Schema>NWMLS:EverNet:ImageData:1.0</Schema></Results></ImageQuery>'


LISTING_QUERY = '<EverNetQuerySpecification xmlns="urn:www.nwmls.com/Schemas/General/EverNetQueryXML.xsd"><Message><Head><UserId>{UserId}</UserId><Password>{Password}</Password><SchemaName>StandardXML1_2</SchemaName></Head><Body><Query>{Query}</Query><Filter>{Filter}</Filter></Body></Message></EverNetQuerySpecification>'

def _validate_query(query, valid_fields):
    for i, v in query.iteritems():
        if i not in valid_fields:
            raise ValueError("Invalid field %s" % i)


def _build_query(query):
    tag = '<{tag}>{value}</{tag}>'
    return ''.join([tag.format(tag=i, value=v) for i, v in query.items()])


def listing_query(username, password, query, filter=''):
    _validate_query(query, VALID_LISTING_QUERY_FIELDS)

    return LISTING_QUERY.format(
        UserId=username,
        Password=password,
        Query=_build_query(query),
        Filter=filter
    )


def photo_query(username, password, listing_number):

    return PHOTO_QUERY.format(
        UserId=username,
        Password=password,
        ListingNumber=listing_number,
    )
