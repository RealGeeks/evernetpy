import datetime
from os import environ
from evernetpy.client import EvernetClient

def _test_query_string():
    username = environ.get('EVERNET_USERNAME')
    password = environ.get('EVERNET_PASSWORD')
    begin_date = (datetime.datetime.utcnow() - datetime.timedelta(hours=10)).strftime('%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    return '''<EverNetQuerySpecification xmlns="urn:www.nwmls.com/Schemas/General/EverNetQueryXML.xsd"><Message>
        <Head><UserId>{username}</UserId><Password>{password}</Password><SchemaName>StandardXML1_2</SchemaName></Head>
        <Body><Query><MLS>nwmls</MLS><PropertyType>RESI</PropertyType><BeginDate>{begin_date}</BeginDate><EndDate>{end_date}</EndDate></Query><Filter></Filter></Body>
        </Message></EverNetQuerySpecification>'''.format(username = username, password =  password, begin_date=begin_date, end_date=end_date)


def test_client():
    test_query = _test_query_string()
    client = EvernetClient('RetrieveListingData')
    results = client.listing_query(test_query)
    assert results
