import hmac, hashlib, unittest
from time import time

try:
    import urllib.parse
except ImportError:
    import urllib

from bsdapi.URL import URL


try:
    url_quote = urllib.parse.quote
except AttributeError:
    url_quote = urllib.quote


class RequestGenerator(object):

    def __init__(self, api_id, api_secret, api_host, https=False):
        self.api_id = api_id
        self.api_secret = api_secret
        self.api_host = api_host
        self.https = https
        self.api_base   = '/page/api'

    def _query_str(self, api_ts, api_params, quote=False):
        quote_func = url_quote if quote else lambda x: x

        api_params.extend([
            ('api_ver', '1'),
            ('api_id', self.api_id),
            ('api_ts', str(api_ts)),])
        return '&'.join(["%s=%s" % (k, quote_func(v)) for k, v in api_params])

    def _signing_string(self, api_ts, api_call, api_params):
        string = "\n".join([
            self.api_id,
            str(api_ts),
            u"%s%s" % (self.api_base, api_call),
            self._query_str(api_ts, api_params, quote=False)])
        return hmac.new(self.api_secret.encode(), string.encode(), hashlib.sha1).hexdigest()

    def get_url(self, api_call, api_params = []):
        params = sorted(api_params.items())
        unix_ts = int(time())
        params.append(('api_mac', self._signing_string(unix_ts, api_call, params)))

        protocol = 'https' if self.https else 'http'
        query = self._query_str(unix_ts, params, quote=True)
        path = u"%s%s" % (self.api_base, api_call)
        return URL(protocol=protocol, host=self.api_host, path=path, query=query)


class TestRequestGenerator(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'
        self.secret = '7405d35963605dc36702c06314df85db7349613f'
        self.api_id = 'sfrazer'

    def test_hmacGenerateProperlyWhenAPIHasNoParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request._signing_string('1272659462', '/circle/list_circles', [])
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

    def test_hmacGenerateProperlyWhenAPIHasParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        params = [('cons_ids', '1,2,3,4,5')]
        signing_string = request._signing_string('1272662274', '/cons/get_constituents_by_id', params)
        self.assertEqual(signing_string, 'c2af877085bcb5390aed0c8256b14ad05f2e3ef1')


if __name__ == '__main__':
    unittest.main()
