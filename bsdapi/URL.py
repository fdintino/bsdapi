import unittest

try:
    import urllib.parse
except ImportError:
    import urllib

try:
    urlencode = urllib.urlencode
except AttributeError:
    urlencode = urllib.parse.urlencode


class URL(object):

    def __init__(self, protocol='http', host='localhost', path='/', query=None):
        self.protocol = protocol
        self.host = host
        self.path = path
        self.query = query

        if isinstance(self.query, dict):
            self.query = urlencode(self.query)
        if self.path[0] != '/':
            self.path = '/' + self.path

    def __str__(self):
        url = self.protocol + '://' + self.host + self.path
        if self.query and len(self.query):
            url = url + '?' + self.query
        return url

    def get_path_and_query(self):
        url = self.path
        if self.query and len(self.query):
            url = url + '?' + self.query
        return url


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'

    def test_GenerateProperURLWithAllElements(self):
        url = URL(host='test.com', path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingProtocol(self):
        url = URL(host='test.com', path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingHost(self):
        url = URL(path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')
    
    def test_GenerateProperURLWithQueryHash(self):
        url = URL(path='/a/b/c', query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingPath(self):
        url = URL(query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/?a=1&b=2')
    
    def test_GenerateProperURLWhenPathDoesntStartWithASlash(self):
        url = URL(path='/a/b/c', query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWhenAllParamsArentSet(self):
        url = URL()
        self.assertEqual(str(url), 'http://localhost/')


if __name__ == '__main__':
    unittest.main()
