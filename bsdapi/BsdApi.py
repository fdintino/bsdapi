from bsdapi.Bundles import Bundles
from bsdapi.Filters import Filters
from bsdapi.RequestGenerator import RequestGenerator
from bsdapi.Styler import Colorizer
from bsdapi.ApiResult import api_result_factory, ApiResultPrettyPrintable

try:
    import http.client as httplib
    from http.client import HTTPException
except ImportError:
    import httplib
    from httplib import HTTPException

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import base64, email.parser


class BsdApi(object):

    GET = 'GET'
    POST = 'POST'

    def __init__(self, id, secret, host, result_cls=None, port=80, secure_port=443, http_username=None, http_password=None):
        self.api_id = id
        self.api_secret = secret
        self.api_host = host
        if result_cls is None:
            result_cls = api_result_factory()

        self.api_result_cls = result_cls
        self.api_port = port
        self.api_secure_port = secure_port
        self.http_username = http_username
        self.http_password = http_password

    def get_deferred_results(self, deferred_id):
        query = {'deferred_id': deferred_id}
        url_secure = self._generate_request('/get_deferred_results', query)
        return self._make_get_request(url_secure)

    def do_request(self, api_call, api_params=None, request_type=GET, body=None, headers=None, https=False):
        if api_params is None:
            api_params = {}

        url = self._generate_request(api_call, api_params, https)

        if request_type == "GET":
            return self._make_get_request(url, https)
        else:
            return self._make_post_request(url, body, https)

    def account_check_credentials(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generate_request('/account/check_credentials', query, https=True)
        return self._make_get_request(url_secure, https = True)

    def account_create_account(self, email, password, firstname, lastname, zip):
        query = {
            'email': email,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'zip': zip,}
        url_secure = self._generate_request('/account/create_account', query, https=True)
        return self._make_get_request(url_secure, https = True)

    def account_reset_password(self, userid):
        query = {'userid': userid}
        url_secure = self._generate_request('/account/reset_password', query, https=True)
        return self._make_get_request(url_secure, https = True)

    def account_set_password(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generate_request('/account/set_password', query, https=True)
        return self._make_get_request(url_secure, https = True)

    def circle_list_circles(self, circle_type=None, state_cd=None):
        query = {}

        if circle_type:
            query['circle_type'] = str(circle_type)

        if state_cd:
            query['state_cd'] = str(state_cd)

        url_secure = self._generate_request('/circle/list_circles', query)
        return self._make_get_request(url_secure)

    def circle_get_cons_ids_for_circle(self, circle_id):
        query = {'circle_id': str(circle_id)}
        url_secure = self._generate_request('/circle/get_cons_ids_for_circle', query)
        return self._make_get_request(url_secure)

    def circle_get_ext_ids_for_circle(self, circle_id, ext_type):
        query = {'circle_id': str(circle_id), 'ext_type': ext_type}
        url_secure = self._generate_request('/circle/get_ext_ids_for_circle', query)
        return self._make_get_request(url_secure)

    def circle_set_cons_ids_for_circle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/circle/set_cons_ids_for_circle')
        return self._make_get_request(url_secure, query)

    def circle_set_ext_ids_for_circle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generate_request('/circle/set_ext_ids_for_circle')
        return self._make_post_request(url_secure, query)

    def circle_add_cons_ids_for_circle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/circle/add_cons_ids_for_circle')
        return self._make_get_request(url_secure, query)

    def circle_add_ext_ids_for_circle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generate_request('/circle/add_ext_ids_for_circle')
        return self._make_get_request(url_secure, query)

    def circle_remove_cons_ids_for_circle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/circle/remove_cons_ids_for_circle')
        return self._make_post_request(url_secure, query)

    def circle_remove_ext_ids_for_circle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generate_request('/circle/remove_ext_ids_for_circle')
        return self._make_post_request(url_secure, query)

    def circle_move_cons_ids_for_circle(self, from_circle_id, to_circle_id, cons_ids):
        query = {'from_circle_id': str(from_circle_id),
                 'to_circle_id': str(to_circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/circle/move_cons_ids_for_circle')
        return self._make_post_request(url_secure, query)

    def circle_move_ext_ids_for_circle(self, from_circle_id, to_circle_id,
                                       ext_type, ext_ids):
        query = {'from_circle_id': str(from_circle_id),
                 'to_circle_id': str(to_circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generate_request('/circle/move_ext_ids_for_circle')
        return self._make_post_request(url_secure, query)

    def circle_set_circle_administrator(self, circle_id, cons_id):
        query = {'circle_id': str(circle_id),
                 'cons_id': str(cons_id)}

        url_secure = self._generate_request('/circle/set_circle_administrator')
        return self._make_post_request(url_secure, query)

    def circle_demote_circle_administrator(self, circle_id, cons_id):
        query = {'circle_id': str(circle_id),
                 'cons_id': str(cons_id)}

        url_secure = self._generate_request('/circle/demote_circle_administrator')
        return self._make_post_request(url_secure, query)

    def circle_set_circle_owner(self, circle_id, cons_id):
        query = {'circle_id': str(circle_id),
                 'cons_id': str(cons_id)}

        url_secure = self._generate_request('/circle/set_circle_owner')
        return self._make_post_request(url_secure, query)

    def cons_get_constituents(self, filter, bundles=None):
        query = {'filter': str(Filters(filter))}

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generate_request('/cons/get_constituents', query)
        return self._make_get_request(url_secure)

    def cons_get_constituents_by_id(self, cons_ids, filter=None, bundles=None):
        '''Retrieves constituents by ID '''
        query = {'cons_ids': ','.join([str(elem) for elem in cons_ids])}

        if filter:
            query['filter'] =  str(Filters(filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generate_request('/cons/get_constituents_by_id', query)
        return self._make_get_request(url_secure)

    def cons_get_constituents_by_ext_id(self, ext_type, ext_ids, filter=None, bundles=None):
        query = {'ext_type': ext_type, 'ext_ids': ','.join([str(elem) for elem in ext_ids])}

        if filter:
            query['filter'] =  str(Filters(filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generate_request('/cons/get_constituents_by_ext_id', query)
        return self._make_get_request(url_secure)

    def cons_get_updated_constituents(self, changed_since, filter=None, bundles=None):
        query = {'changed_since': str(changed_since)}

        if filter:
            query['filter'] =  str(Filters(filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generate_request('/cons/get_updated_constituents', query)
        return self._make_get_request(url_secure)

    def cons_set_ext_ids(self, ext_type, cons_id__ext_id):
        query = {'ext_type': str(ext_type)}
        query.update(cons_id__ext_id)
        url_secure = self._generate_request('/cons/set_ext_ids')
        return self._make_post_request(url_secure, query)

    def cons_delete_constituents_by_id(self, cons_ids):
        query = {'cons_ids': ','.join([str(cons) for cons in cons_ids])}
        url_secure = self._generate_request('/cons/delete_constituents_by_id')
        return self._make_post_request(url_secure, query)

    def cons_get_bulk_constituent_data(self, format, fields, cons_ids=None, filter=None):
        query = {'format': str(format), 'fields': ','.join([str(field) for field in fields])}

        if cons_ids:
            query['cons_ids'] = ','.join([str(cons) for cons in cons_ids])

        if filter:
            query['filter'] =  str(Filters(filter))

        url_secure = self._generate_request('/cons/get_bulk_constituent_data', {})
        return self._make_post_request(url_secure, query)

    def cons_set_constituent_data(self, xml_data):
        url_secure = self._generate_request('/cons/set_constituent_data')
        return self._make_post_request(url_secure, xml_data)

    def cons_get_custom_constituent_fields(self):
        query = {}
        url_secure = self._generate_request('/cons/get_custom_constituent_fields', query)
        return self._make_get_request(url_secure)

    def cons_merge_constituents_by_id(self, ids):
        url_secure = self._generate_request('/cons/merge_constituents_by_id')
        return self._make_post_request(url_secure, ','.join([str(x) for x in ids]))

    def cons_merge_constituents_by_email(self, email):
        url_secure = self._generate_request('/cons/merge_constituents_by_email', {'email': email})
        return self._make_get_request(url_secure)

    def cons_group_list_constituent_groups(self):
        url_secure = self._generate_request('/cons_group/list_constituent_groups')
        return self._make_get_request(url_secure)

    def cons_group_get_constituent_group(self, cons_group_id):
        query = {'cons_group_id': str(cons_group_id)}
        url_secure = self._generate_request('/cons_group/get_constituent_group', query)
        return self._make_get_request(url_secure)

    def cons_group_add_constituent_group(self, xml_data):
        url_secure = self._generate_request('/cons_group/add_constituent_groups')
        return self._make_post_request(url_secure, xml_data)

    def cons_group_delete_constituent_groups(self, cons_group_ids):
        query = {'cons_group_ids': ','.join([str(c) for c in cons_group_ids])}
        url_secure = self._generate_request('/cons_group/delete_constituent_groups', query)
        return self._make_get_request(url_secure)

    def cons_group_get_cons_ids_for_group(self, cons_group_id):
        query = {'cons_group_id': str(cons_group_id)}
        url_secure = self._generate_request('/cons_group/get_cons_ids_for_group', query)
        return self._make_get_request(url_secure)

    def cons_group_get_ext_ids_for_group(self, cons_group_id, ext_type):
        query = {'cons_group_ids': str(cons_group_id), 'ext_type': ext_type}
        url_secure = self._generate_request('/cons_group/get_ext_ids_for_group', query)
        return self._make_get_request(url_secure)

    def cons_group_set_ext_ids_for_group(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generate_request('/cons_group/set_ext_ids_for_group')
        return self._make_post_request(url_secure, query)

    def cons_group_add_cons_ids_to_group(self, cons_group_id, cons_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/cons_group/add_cons_ids_to_group')
        return self._make_post_request(url_secure, query)

    def cons_group_add_ext_ids_to_group(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generate_request('/cons_group/add_ext_ids_to_group')
        return self._make_post_request(url_secure, query)

    def cons_group_remove_cons_ids_from_group(self, cons_group_id, cons_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generate_request('/cons_group/remove_cons_ids_from_group')
        return self._make_post_request(url_secure, query)

    def cons_group_remove_ext_ids_from_group(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generate_request('/cons_group/remove_ext_ids_from_group')
        return self._make_post_request(url_secure, query)

    def event_rsvp_list(self, event_id):
        query = {'event_id': str(event_id)}
        url_secure = self._generate_request('/event/list_rsvps')
        return self._make_post_request(url_secure, query)

    def outreach_get_page_by_id(self, id):
        query = {'id': str(id)}
        url_secure = self._generate_request('/outreach/get_page_by_id')
        return self._make_post_request(url_secure, query)

    def outreach_set_page_data(self, xml_data):
        url_secure = self._generate_request('/outreach/set_page_data', {})
        return self._make_post_request(url_secure, xml_data)

    def reference_process_personalization_tag(self, who):
        url_secure = self._generate_request('/reference/process_personalization_tag', {'who': who})
        return self._make_get_request(url_secure)

    def signup_process_signup(self, xml_data):
        query = {}
        url_secure = self._generate_request('/signup/process_signup', query)
        return self._make_post_request(url_secure, xml_data)

    def signup_list_forms(self):
        query = {}
        url_secure = self._generate_request('/signup/list_forms', query, True)
        return self._make_get_request(url_secure, True)

    def signup_list_form_fields(self, signup_form_id):
        query = {'signup_form_id': str(signup_form_id)}
        url_secure = self._generate_request('/signup/list_form_fields', query)
        return self._make_get_request(url_secure)

    def signup_signup_count(self, signup_form_id, signup_form_field_ids=None):
        query = {'signup_form_id': str(signup_form_id)}

        if signup_form_field_ids:
            query['signup_form_field_ids'] = ','.join([str(elem) for elem in signup_form_field_ids])

        url_secure = self._generate_request('/signup/signup_count', query)
        return self._make_get_request(url_secure)

    def signup_count_by_field(self, signup_form_id, signup_form_field_id):
        query = {'signup_form_id': str(signup_form_id),
                 'signup_form_field_id': str(signup_form_field_id)}

        url_secure = self._generate_request('/signup/count_by_field', query)
        return self._make_get_request(url_secure)

    def wrappers_list_wrappers(self):
        url_secure = self._generate_request('/wrappers/list_wrappers')
        return self._make_get_request(url_secure)

    def _make_request(self, url_secure, request_type, http_body=None, headers=None, https=False):
        connect_function = httplib.HTTPSConnection if https else httplib.HTTPConnection
        port = self.api_secure_port if https else self.api_port

        connection = connect_function(self.api_host, port)

        if headers == None:
            headers = dict()

        headers['User-Agent'] = 'Python API'

        if self.http_username:
            auth_string = self.http_username
            if self.http_password:
                auth_string += ":" + self.http_password
            headers["Authorization"] = "Basic " + base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        if http_body != None and headers != None:
            connection.request(request_type, url_secure.get_path_and_query(), http_body, headers)
        elif headers != None:
            connection.request(request_type, url_secure.get_path_and_query(), None, headers)
        else:
            connection.request(request_type, url_secure.get_path_and_query())
        response = None
        try:
            response = connection.getresponse()
            headers = response.getheaders()
            body_bytes = response.read()
            content_type, charset = self._parse_content_type(
                response.getheader('Content-Type',
                    default='application/json; charset=iso-8859-1'))
            body = body_bytes.decode(charset)

            connection.close()

            results = self.api_result_cls(url_secure, response, headers, body)
            return results
        except HTTPException as error:
            print(error)
            print("Error calling " + url_secure.get_path_and_query())

    def _parse_content_type(self, content_type_header, default_charset='iso-8859-1'):
        parsed_headers = email.parser.Parser().parsestr(
            "Content-Type: %s" % content_type_header, headersonly=True)
        charset = default_charset
        if parsed_headers.get_param('charset') is not None:
            charset = parsed_headers.get_param('charset')
        return (parsed_headers.get_content_type(), charset)

    def _generate_request(self, api_call, api_params=None, https=False):
        if api_params is None:
            api_params = {}

        api_host = self.api_host

        if https:
            if self.api_secure_port != 443:
                api_host = api_host + ':' + str(self.api_secure_port)
        else:
            if self.api_port != 80:
                api_host = api_host + ":" + str(self.api_port)

        request = RequestGenerator(self.api_id, self.api_secret, api_host, https)
        url_secure = request.get_url(api_call, api_params)
        return url_secure

    def _make_get_request(self, url_secure, https=False):
        return self._make_request(url_secure, self.GET, https=https)

    def _make_post_request(self, url_secure, body, https=False):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/xml"}

        if type(body).__name__ == 'dict':
            http_body = urlencode(body)
        else:
            http_body = body

        return self._make_request(url_secure, self.POST, http_body, headers, https)

class Factory(object):

    def create(self, id, secret, host, port, secure_port, colorize=False):
        styler = Colorizer(ansi_colors=colorize)
        api_result_cls = api_result_factory(ApiResultPrettyPrintable(styler))
        return BsdApi(id, secret, host, api_result_cls, port, secure_port)
