Blue State Digital Interactive API
==================================

Requirements
------------
* The BSD API is written in [Python 3](http://www.python.org/download/releases/3.0/) and requires Python 3+ to be installed on the host.

Installing
----------
The easiest way to get up and running is to download the source, and from the directory with the source code, run:

    /path/to/python3 Console.py --file=api.cfg

The file api.cfg can be created from the sample.cfg file in the same directory. See the next section about how to write the configuration file.

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

Usage
-----
To display usage options use the `--help` flag

    Usage: Console.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -v, --verbose         Makes this tool loud and obnoxious.
      -c, --color           Use ANSI colors for display
      -f CONFIG_FILE, --file=CONFIG_FILE
                            The Configuration File

Raw API Call Example
--------------------
The following walks through making a simple API call to list out all signup forms using the BSD Interactive API shell.

First start the shell.

    /path/to/python3 Console.py --file=api.cfg
    BSD Interactive API
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.doRequest('/signup/list_forms', {}, api.GET, None))
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

Raw API Method
--------------
To issue a raw API request use the `api.doRequest` method, which will always return a `BsdApiResults` object. This method accepts 4 parameters as listed below:

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

    /path/to/python3 Console.py --file=api.cfg
    BSD Interactive API
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.signup_listForms())
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
    * `cons_getConstituents(filter, bundles=None)`
    * `cons_getConstituentsById(cons_ids, filter=None, bundles=None)`
    * `cons_getConstituentsByExtId(ext_type, ext_ids, filter=None, bundles=None)`
    * `cons_getUpdatedConstituents(changed_since, filter=None, bundles=None)`
    * `cons_setExtIds(ext_type, cons_id__ext_id)`
    * `cons_deleteConstituentsById(cons_ids)`
    * `cons_getBulkConstituentData(format, fields, cons_ids=None, filter=None)`
    * `cons_setConstituentData(xml_data)`
* **Constituent Group (cons_group) API Calls**
    * `cons_group_listConstituentGroups()`
    * `cons_group_getConstituentGroup(cons_group_id)`
    * `cons_group_addConstituentGroup(xml_data)`
    * `cons_group_deleteConstituentGroup(cons_group_ids)`
    * `cons_group_getConsIdsForGroup(cons_group_id)`
    * `cons_group_getExtIdsForGroup(cons_group_id, ext_type)`
    * `cons_group_setExtIdsForGroup(cons_group_id, ext_type, ext_ids)`
    * `cons_group_addConsIdsToGroup(cons_group_id, cons_ids)`
    * `cons_group_addExtIdsToGroup(cons_group_id, ext_type, ext_ids)`
    * `cons_group_removeConsIdsToGroup(cons_group_id, cons_ids)`
    * `cons_group_removeExtIdsToGroup(cons_group_id, ext_type, ext_ids)`
* **Circle (circle) API Calls**
    * `circle_listCircles(circle_type=None, state_cd=None)`
    * `circle_getConsIdsForCircle(circle_id)`
    * `circle_getExtIdsForCircle(circle_id, ext_type)`
    * `circle_setConsIdsForCircle(circle_id, cons_ids)`
    * `circle_setExtIdsForCircle(circle_id, ext_type, ext_ids)`
    * `circle_addConsIdsForCircle(circle_id, cons_ids)`
    * `circle_addExtIdsForCircle(circle_id, ext_type, ext_ids)`
    * `circle_removeConsIdsForCircle(circle_id, cons_ids)`
    * `circle_removeExtIdsForCircle(circle_id, ext_type, ext_ids)`
    * `circle_moveConsIdsForCircle(from_circle_id, to_circle_id, cons_ids)`
    * `circle_moveExtIdsForCircle(from_circle_id, to_circle_id, ext_type, ext_ids)`
    * `circle_setCircleAdministrator(circle_id, cons_id)`
    * `circle_demoteCircleAdministrator(circle_id, cons_id)`
    * `circle_setCircleOwner(circle_id, cons_id)`
* **Signup (signup) API Calls**
    * `signup_listForms()`
    * `signup_listFormFields(signup_form_id)`
    * `signup_signupCount(signup_form_id, signup_form_field_ids=None)`
    * `signup_countByField(signup_form_id, signup_form_field_id)`
    * `signup_form_id, signup_form_field_id`
* **Outreach (outreach) API Calls**
    * `outreach_getPageById(outreach_page_id)`
    * `outreach_setPageData(xml_data)`
* **Wrappers (wrappers) API Calls**
    * `wrappers_listWrappers()`
* **VAN API Calls**
* **VAN Campaign API Calls**
* **Account API Calls**
    * `account_checkCredentials(userid, password)`
    * `account_createAccount(email, password, firstname, lastname, zip)`
    * `account_resetPassword(userid)`
    * `account_setPassword(userid, password)`
* **Deferred Results API Calls**
    * `getDeferredResults(deferred_id)`
