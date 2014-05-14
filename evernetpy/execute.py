import logging
from client import EvernetClient
from query import listing_query, photo_query
from parser import parse

logger = logging.getLogger(__name__)


def execute_listing_query(username, password, endpoint, params, filter=""):
    client = EvernetClient(endpoint)
    query = listing_query(username, password, params, filter)
    logger.info('Executing query %s with params %s...' % (endpoint, params))
    data = client.listing_query(query)
    logger.info('got results')
    return parse(data)


def execute_photo_query(username, password, listing_number):
    client = EvernetClient('RetrieveImages')
    query = photo_query(username, password, listing_number)
    logger.info('Executing photo query for listing number %s' % listing_number)
    data = client.photo_query(query)
    logger.info('got results')
    return parse(data)
