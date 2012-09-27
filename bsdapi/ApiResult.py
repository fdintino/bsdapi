import json


class ApiResultPrettyPrintable(object):

    def __init__(self, styler):
        self.styler = styler

    def to_string(self, api_result):
        if api_result.http_status == 200:
            color = 'green'
        elif api_result.http_status == 202:
            color = 'yellow'
        else:
            color = 'red'

        status_str = "%s %s %s" % (api_result.http_version, str(api_result.http_status), api_result.http_reason)
        headers_str = '\n'.join(['%s: %s' % (k, v) for k, v in api_result.headers]) + '\n'

        ''' assume json response body and try to prettyprint, just print plain
        response if fail'''
        try:
            body_str = json.dumps(json.loads(api_result.body), sort_keys=True, indent=4)
        except:
            body_str = api_result.body

        full_str = "%s\n%s\n%s" % (self.styler.color(status_str, color),
                self.styler.color(headers_str, 'purple'),
                body_str)
        return full_str.strip()


class BaseApiResult(object):

    stringizer = None

    def __init__(self, request_url, http_response, headers, body):
        self.s = http_response
        self.http_status = http_response.status
        self.http_reason = http_response.reason
        self.http_version = ('HTTP/1.0' if http_response.version == 10 else 'HTTP/1.1')
        self.request_url = request_url
        self.http_response = http_response
        self.headers = headers
        self.body = body

    def __str__(self):
        return repr(self)


def api_result_factory(stringizer=None):
    attrs = {}
    to_string = getattr(stringizer, 'to_string', None)
    if to_string is not None:
        attrs['__str__'] = lambda self: to_string(self)

    return type("ApiResult", (BaseApiResult,), attrs)
