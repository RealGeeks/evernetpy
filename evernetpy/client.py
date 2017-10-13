from xml.sax.saxutils import escape
import tempfile
import logging
from xml.parsers.expat import ParserCreate, ExpatError
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# set up requests retries
session = requests.Session()
retry = Retry(
    total=3,
    read=3,
    connect=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)


class EvernetClient(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def _start_element_get_envelope(self, name, attrs):
        if name == self.endpoint + 'Result':
            self.in_envelope = True

    def _end_element_get_envelope(self, name):
        if name == self.endpoint + 'Result':
            self.in_envelope = False

    def _char_data_get_envelope(self, data):
        self.data.write(data.encode('utf-8'))

    def listing_query(self, query):
        data = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.nwmls.com/EverNetServices" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><ns0:Body><ns1:{0}><ns1:v_strXmlQuery>{1}</ns1:v_strXmlQuery></ns1:{0}></ns0:Body></SOAP-ENV:Envelope>'.format(self.endpoint, escape(str(query)))

        response = session.post('http://evernet.nwmls.com/evernetqueryservice/evernetquery.asmx', headers = {
            'Soapaction': "http://www.nwmls.com/EverNetServices/{0}".format(self.endpoint),
            'Content-Type': 'text/xml; charset=utf-8',
        }, timeout=60*5, data=data, stream=True)

        logger.info('Sent request...')
        logger.debug('>>> %s' % data)

        with tempfile.TemporaryFile() as response_file:
            tmp = response.raw.read(1000)
            logger.info('Receiving data...')
            while tmp:
                response_file.write(tmp)
                tmp = response.raw.read(1000)
                logger.debug('<<< %s' % tmp)
            response_file.seek(0)

            self.data = tempfile.TemporaryFile()
            self.in_envelope = False
            p = ParserCreate()
            p.StartElementHandler = self._start_element_get_envelope
            p.EndElementHandler = self._end_element_get_envelope
            p.CharacterDataHandler = self._char_data_get_envelope
            response_file.seek(0)
            try:
                p.ParseFile(response_file)
            except ExpatError:
                logging.error("Error parsing XML response from Evernet.  This usually happens when the server returns an error message.  You can see the full response if you set the logging to DEBUG level")
                raise
        logger.info('All data received, starting parsing')
        self.data.seek(0)
        return self.data

    def photo_query(self, query):
        data = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><RetrieveImages xmlns="NWMLS:EverNet"><query>{0}</query></RetrieveImages></soap:Body></soap:Envelope>'.format(escape(query))
        response = session.post('http://images.idx.nwmls.com/imageservice/imagequery.asmx', headers = {
          'Content-Type': 'text/xml; charset=utf-8',
          'Soapaction':'NWMLS:EverNet/RetrieveImages',
        }, data=data, timeout=30, stream=True)
        logger.debug('>>> %s' % data)

        with tempfile.TemporaryFile() as response_file:
            tmp = response.raw.read(1000)
            while tmp:
                response_file.write(tmp)
                tmp = response.raw.read(1000)
                logger.debug('<<< %s' % tmp)
            response_file.seek(0)

            self.data = tempfile.TemporaryFile()
            self.in_envelope = False
            p = ParserCreate()
            p.StartElementHandler = self._start_element_get_envelope
            p.EndElementHandler = self._end_element_get_envelope
            p.CharacterDataHandler = self._char_data_get_envelope
            p.ParseFile(response_file)
        self.data.seek(0)
        return self.data
