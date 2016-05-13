from xml.sax.saxutils import escape
import httplib
import tempfile
import logging
from xml.parsers.expat import ParserCreate, ExpatError

logger = logging.getLogger(__name__)


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
        import socket
        socket.setdefaulttimeout(60 * 5)
        conn = httplib.HTTPConnection('evernet.nwmls.com', timeout=60 * 5)
        conn.putrequest('POST', '/evernetqueryservice/evernetquery.asmx')
        conn.putheader('Soapaction', u'"http://www.nwmls.com/EverNetServices/{0}"'.format(self.endpoint))
        conn.putheader('Content-Type', 'text/xml; charset=utf-8')
        conn.putheader('Content-Length', '%d' % len(data))
        conn.endheaders()
        conn.send(data)
        logger.info('Sent request...')
        logger.debug('>>> %s' % data)

        with tempfile.TemporaryFile() as response_file:
            response = conn.getresponse()
            tmp = response.read(1000)
            logger.info('Receiving data...')
            while tmp:
                response_file.write(tmp)
                tmp = response.read(1000)
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
        import socket
        socket.setdefaulttimeout(30)
        conn = httplib.HTTPConnection('images.idx.nwmls.com', timeout=30)
        conn.putrequest('POST', '/imageservice/imagequery.asmx')
        conn.putheader('Content-Type', 'text/xml; charset=utf-8')
        conn.putheader('Soapaction', 'NWMLS:EverNet/RetrieveImages')
        conn.putheader('Content-Length', '%d' % len(data))
        conn.endheaders()
        conn.send(data)
        logger.debug('>>> %s' % data)

        with tempfile.TemporaryFile() as response_file:
            response = conn.getresponse()
            tmp = response.read(1000)
            while tmp:
                response_file.write(tmp)
                tmp = response.read(1000)
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
