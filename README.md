Blue State Digital API Client
=============================

Requirements
------------

* Python 2.7+

Installing
----------

    $ cd /path/to/setup.py
    $ python setup.py install

The executable's path might not be in your PATH.  In the output for the installer, there is a line that says where the executable is located.  It should say something like 'Installing bsdapi script to /home/sfrazer/bin'.

Configuration File
------------------
The configuration file describes how to connect to your API host and the credentials by which to authenticate. All data needed for this configuration file can be obtained from the Control Panel under **Advanced** -> **Manage API Users**. A sample configuration file is listed below

    [basic]
    host: your-site.com
    port: 80
    username: basic_user
    password: basic_pass
    api_id: your_api_id
    secret: 74d5d37963105dc36702f0631adf85db7389613f

The `api_id` and `secret` are taken directly from the Manage API Users page.

The username and password fields are only if HTTP basic authentication is required to access the API.  For most cases, these variables can be left out.

Usage
-----
To display usage options use the `--help` flag

    $ bsdapi --help
    usage: bsdapi [-h] [-L LOG_LEVEL] [-c] [-v] CONFIG

    Blue State Digital API Client

    positional arguments:
      CONFIG                Configuration file

    optional arguments:
      -h, --help            show this help message and exit
      -L LOG_LEVEL, --log-level LOG_LEVEL
                            'debug', 'error', 'warning', 'info', or 'critical'
      -c, --color           Display with ANSI terminal colors.
      -v, --verbose         Show verbose output.

    (c) 2011 Blue State Digital

Raw API Call Example
--------------------
The following walks through making a simple API call to list out all signup forms using the BSD Interactive API shell.

First start the shell.

    $ bsdapi /path/to/config.cfg
    Blue State Digital API Client
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.do_request('/signup/list_forms', {}, api.GET, None))
    HTTP/1.1 200 OK
    Date: Tue, 15 Jun 2010 18:21:54 GMT
    Server: Apache/2.0.63 (Unix) mod_ssl/2.0.63 OpenSSL/0.9.7g PHP/5.2.6
    X-Powered-By: PHP/5.2.6
    Content-Length: 2134
    Content-Type: application/xml; charset=utf-8

    <?xml version="1.0" encoding="UTF-8"?>
    <api>
        <signup_form id="1" modified_dt="1267728690">
            <signup_form_name>Default Signup Form</signup_form_name>
            <signup_form_slug/>
            <form_public_title>This is the public form title</form_public_title>
            <create_dt>2010-02-08 18:33:11</create_dt>
        </signup_form>
        <signup_form id="3" modified_dt="1269523250">
            <signup_form_name>signup form</signup_form_name>
            <signup_form_slug>form</signup_form_slug>
            <form_public_title>This is a signup form</form_public_title>
            <create_dt>2010-03-25 13:20:50</create_dt>
        </signup_form>
    </api>

Python Library Usage
--------------------

The bsdapi can be included as a module and used to build larger applications.  Building a `BsdApi` object is simple using the the factory:

```python
from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from bsdapi.BsdApi import Factory as BsdApiFactory

api = BsdApiFactory().create(
    id='sfrazer',
    secret='8c0c28988dba57865bc8f6d6aa7de7230cfa42d6',
    host='sandgate.bluestatedigital.com',
    port=8174,
    secure_port=9174)

api_result = api.signup_list_forms()
tree = ElementTree().parse( StringIO(api_result.body) )

print('All Signup Forms:')
for index, signup_form in enumerate(tree.findall('signup_form')):
        print('%d.  %s' % (index+1, signup_form.find('signup_form_name').text))
```

Raw API Method
--------------
To issue a raw API request use the `api.do_request` method, which will always return a `ApiResult` object. This method accepts 4 parameters as listed below:

* **api_call**

  *Required*

  The RESTful url of the API call without the `/page/api` part.

* **api_params**

  *Optional* -- defaults to `{}`

  The parameters to pass to the API.

* **request_type**

  *Optional* -- defaults to `api.GET`

  The method to use to submit the RESTful call. Can be either `api.GET` or `api.POST`

* **body**

  *Optional* -- defaults to `None`

  You can set the body of a POST request by specifying the fourth parameter.

* **headers**

  *Optional* -- defaults to `None`

* **https**

  *Optional* -- defaults to `False`

  Set this to `True` to send the API call securely using SSL.

API Call Using Helper Methods Example
-------------------------------------
The following walks through making a simple API call to list out all signup forms using the helper methods included with the BSD Interactive API shell.

First start the shell.

    $ bsdapi /path/to/config.cfg
    Blue State Digital API Client
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.signup_list_forms())
    HTTP/1.1 200 OK
    Date: Tue, 15 Jun 2010 18:21:54 GMT
    Server: Apache/2.0.63 (Unix) mod_ssl/2.0.63 OpenSSL/0.9.7g PHP/5.2.6
    X-Powered-By: PHP/5.2.6
    Content-Length: 2134
    Content-Type: application/xml; charset=utf-8

    <?xml version="1.0" encoding="UTF-8"?>
    <api>
        <signup_form id="1" modified_dt="1267728690">
            <signup_form_name>Default Signup Form</signup_form_name>
            <signup_form_slug/>
            <form_public_title>This is the public form title</form_public_title>
            <create_dt>2010-02-08 18:33:11</create_dt>
        </signup_form>
        <signup_form id="3" modified_dt="1269523250">
            <signup_form_name>signup form</signup_form_name>
            <signup_form_slug>form</signup_form_slug>
            <form_public_title>This is a signup form</form_public_title>
            <create_dt>2010-03-25 13:20:50</create_dt>
        </signup_form>
    </api>

API Helper Methods Documentation
--------------------------------
The following methods are available for use. All methods return a `BsdApiResults` object unless noted otherwise.

* **Constituent (cons) API Calls**
    * `cons_get_constituents(filter, bundles=None)`
    * `cons_get_constituents_by_id(cons_ids, filter=None, bundles=None)`
    * `cons_get_constituents_by_ext_id(ext_type, ext_ids, filter=None, bundles=None)`
    * `cons_get_updated_constituents(changed_since, filter=None, bundles=None)`
    * `cons_set_ext_ids(ext_type, cons_id__ext_id)`
    * `cons_delete_constituents_by_id(cons_ids)`
    * `cons_get_bulk_constituent_data(format, fields, cons_ids=None, filter=None)`
    * `cons_set_constituent_data(xml_data)`
* **Constituent Group (cons_group) API Calls**
    * `cons_group_list_constituent_groups()`
    * `cons_group_get_constituent_group(cons_group_id)`
    * `cons_group_add_constituent_group(xml_data)`
    * `cons_group_delete_constituent_group(cons_group_ids)`
    * `cons_group_get_cons_ids_for_group(cons_group_id)`
    * `cons_group_get_ext_ids_for_group(cons_group_id, ext_type)`
    * `cons_group_set_ext_ids_for_group(cons_group_id, ext_type, ext_ids)`
    * `cons_group_add_cons_ids_to_group(cons_group_id, cons_ids)`
    * `cons_group_add_ext_ids_to_group(cons_group_id, ext_type, ext_ids)`
    * `cons_group_remove_cons_ids_to_group(cons_group_id, cons_ids)`
    * `cons_group_remove_ext_ids_to_group(cons_group_id, ext_type, ext_ids)`
* **Circle (circle) API Calls**
    * `circle_list_circles(circle_type=None, state_cd=None)`
    * `circle_get_cons_ids_for_circle(circle_id)`
    * `circle_get_ext_ids_for_circle(circle_id, ext_type)`
    * `circle_set_cons_ids_for_circle(circle_id, cons_ids)`
    * `circle_set_ext_ids_for_circle(circle_id, ext_type, ext_ids)`
    * `circle_add_cons_ids_for_circle(circle_id, cons_ids)`
    * `circle_add_ext_ids_for_circle(circle_id, ext_type, ext_ids)`
    * `circle_remove_cons_ids_for_circle(circle_id, cons_ids)`
    * `circle_remove_ext_ids_for_circle(circle_id, ext_type, ext_ids)`
    * `circle_move_cons_ids_for_circle(from_circle_id, to_circle_id, cons_ids)`
    * `circle_move_ext_ids_for_circle(from_circle_id, to_circle_id, ext_type, ext_ids)`
    * `circle_set_circle_administrator(circle_id, cons_id)`
    * `circle_demote_circle_administrator(circle_id, cons_id)`
    * `circle_set_circle_owner(circle_id, cons_id)`
* **Signup (signup) API Calls**
    * `signup_list_forms()`
    * `signup_list_form_fields(signup_form_id)`
    * `signup_signup_count(signup_form_id, signup_form_field_ids=None)`
    * `signup_count_by_field(signup_form_id, signup_form_field_id)`
    * `signup_form_id, signup_form_field_id`
* **Outreach (outreach) API Calls**
    * `outreach_get_page_by_id(outreach_page_id)`
    * `outreach_set_page_data(xml_data)`
* **Wrappers (wrappers) API Calls**
    * `wrappers_list_wrappers()`
* **VAN API Calls**
* **VAN Campaign API Calls**
* **Account API Calls**
    * `account_check_credentials(userid, password)`
    * `account_create_account(email, password, firstname, lastname, zip)`
    * `account_reset_password(userid)`
    * `account_set_password(userid, password)`
* **Deferred Results API Calls**
    * `get_deferred_results(deferred_id)`
* **Event RSVP API Calls**
    * `event_rsvp_list(event_id)`
