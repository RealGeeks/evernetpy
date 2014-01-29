import pytest
from evernetpy.query import listing_query

def test_listing_query():
    expected = '<EverNetQuerySpecification xmlns="urn:www.nwmls.com/Schemas/General/EverNetQueryXML.xsd"><Message><Head><UserId>username</UserId><Password>password</Password><SchemaName>StandardXML1_2</SchemaName></Head><Body><Query><MLS>nwmls</MLS><PropertyType>RESI</PropertyType></Query><Filter></Filter></Body></Message></EverNetQuerySpecification>'
    assert listing_query('username', 'password', {'MLS':'nwmls', 'PropertyType':'RESI'}) == expected

def test_validate_query():
    with pytest.raises(ValueError):
        assert listing_query('username', 'password', {'FOO':'Bar'})
