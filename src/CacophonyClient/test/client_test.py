# -*- coding: utf-8 -*-
"""Unit tests for the Python client of the  Cacophony Project REST API server.
NB/WARNING:
This module implements tests for the CacophonyClient class
but does so
 + without any server instance running
 + by mocking all the expected responses.
So any change of (response format from) the server will **NOT** be
detected by this module.
See client_test_with_server.py for tests against a running server instance.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import socket
import unittest
import warnings

import json
import mock
import requests
import requests.exceptions
import requests_mock

from nose.tools import raises


from datetime import datetime

from CacophonyClient.client import CacophonyClient

defaults = {
    "apiURL"              : "http://localhost:1080",
    "defaultDevice"       : "test-device",
    "defaultPassword"     : "test-password",
    "defaultGroup"        : "test-group",
    "defaultGroup2"       : "test-group-2",
    "defaultUsername"     : "python-client-user-test",
    "defaultuserPassword" : "test-user_TEST!@#$%-password",
    "filesURL"            : "/files",
    "hostsFileString"     : "`127.0.0.1 raspberrypi::1 localhost"
}

_strToSqlDateTime = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def _build_response_object(status_code=200, content=""):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = content.encode("utf8")
    return resp


def _mocked_session(cli, method="GET", status_code=200, content=""):
    method = method.upper()

    def request(*args, **kwargs):
        """Request content from the mocked session."""
        c = content

        # Check method
        assert method == kwargs.get('method', 'GET')

        if method == 'POST':
            data = kwargs.get('data', None)

            if data is not None:
                # Data must be a string
                assert isinstance(data, str)

                # Data must be a JSON string
                assert c == json.loads(data, strict=True)

                c = data

        # Anyway, Content must be a JSON string (or empty string)
        if not isinstance(c, str):
            c = json.dumps(c)

        return _build_response_object(status_code=status_code, content=c)

    return mock.patch.object(cli._session, 'request', side_effect=request)

class TestCacophonyClient(unittest.TestCase):
    """Set up the TestCacophonyClient object."""

    def setUp(self):
        """Initialize an instance of TestCacophonyClient object."""
        # By default, raise exceptions on warnings
        warnings.simplefilter('error', FutureWarning)
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                "{apiURL}/authenticate_user".format(apiURL=defaults["apiURL"]),
                status_code=204
            )
            cli = CacophonyClient(baseurl=defaults["apiURL"], 
                            username=defaults["defaultUsername"], 
                            password=defaults["defaultuserPassword"])
            print(m.last_request.body)


    def test_scheme(self):
        """Set up the test schema for TestCacophonyClient object."""
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                "{apiURL}/authenticate_user".format(apiURL=defaults["apiURL"]),
                status_code=204
            )
            cli = CacophonyClient(baseurl=defaults["apiURL"], 
                            username=defaults["defaultUsername"], 
                            password=defaults["defaultuserPassword"])
            print(m.last_request.body)
            self.assertEqual(defaults['apiURL'], cli._baseurl)
 


    def test_query(self):
        """Test query in TestCacophonyClient object."""
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                "{apiURL}/authenticate_user".format(apiURL=defaults["apiURL"]),
                status_code=204
            )
            cli = CacophonyClient(baseurl=defaults["apiURL"], 
                           username=defaults["defaultUsername"], 
                           password=defaults["defaultuserPassword"])
            print(m.last_request.body)
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.GET,
                "{apiURL}/api/v1/recordings".format(apiURL=defaults["apiURL"]),
                json={"rows":{'key1': 'value1', 'key2': 'value2'}}, status_code=200
            )
            result = cli.query(
                    endDate=_strToSqlDateTime("2019-11-06 06:30:00"),
                    startDate=_strToSqlDateTime("2019-11-01 19:00:00"),
                    limit=300,
                    offset=0,
                    tagmode="any")

            print(m.last_request.qs)

            self.assertEqual(
                m.last_request.qs,
                {'where': ['{"recordingdatetime": {"$gte": "2019-11-01t19:00:00", "$lte": "2019-11-06t06:30:00"}}'], 'limit': ['300'], 'offset': ['0'], 'tagmode': ['any']}
            )

class FakeClient(CacophonyClient):
    """Set up a fake client instance of CacophonyClient."""

    def __init__(self, *args, **kwargs):
        """Initialize an instance of the FakeClient object."""
        super(FakeClient, self).__init__(*args, **kwargs)
    #TODO: recordings query instead of query
    # def query(self,
    #           query,
    #           params=None,
    #           expected_response_code=200,
    #           database=None):
    #     """Query data from the FakeClient object."""
    #     if query == 'Fail':
    #         raise Exception("Fail")
    #     elif query == 'Fail once' and self._host == 'host1':
    #         raise Exception("Fail Once")
    #     elif query == 'Fail twice' and self._host in 'host1 host2':
    #         raise Exception("Fail Twice")
    #     else:
    #         return "Success"