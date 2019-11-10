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

from datetime import datetime

from CacophonyClient.client import CacophonyClient

defaults = {
    "apiURL"              : "http://localhost:1080",
    "defaultDevice"       : "test-device",
    "defaultPassword"     : "test-password",
    "defaultGroup"        : "test-group",
    "defaultGroup2"       : "test-group-2",
    "defaultUsername"     : "cacophony-client-user-test",
    "defaultuserPassword" : "test-user-password",
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

class mockedCacophonyServer(unittest.TestCase):
    """Test client calls to the mocked CacophonyServer object."""

    def setUp(self):
        """Initialize an instance of mocked CacophonyServer object."""
        # By default, raise exceptions on warnings
        warnings.simplefilter('error', FutureWarning)
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                "{apiURL}/authenticate_user".format(apiURL=defaults["apiURL"]),
                status_code=204
            )
            self.cli = CacophonyClient(baseurl=defaults["apiURL"], 
                            username=defaults["defaultUsername"], 
                            password=defaults["defaultuserPassword"])
            # print("SETUP: last request.body:{}".format(m.last_request.body))


    def test_scheme(self):
        """Set up the test schema for mocked CacophonyServer object."""
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.POST,
                "{apiURL}/authenticate_user".format(apiURL=defaults["apiURL"]),
                status_code=204
            )
            cli = CacophonyClient(baseurl=defaults["apiURL"], 
                            username=defaults["defaultUsername"], 
                            password=defaults["defaultuserPassword"])
            # print(m.last_request.body)
            self.assertEqual(defaults['apiURL'], cli._baseurl)
 


    def test_query(self):
        """Test CacophonyClient.query from mocked CacophonyServer object."""
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.GET,
                "{apiURL}/api/v1/recordings".format(apiURL=defaults["apiURL"]),
                json={"rows":{'key1': 'value1', 'key2': 'value2'}}, status_code=200
            )
            result = self.cli.query(
                    endDate=_strToSqlDateTime("2019-11-06 06:30:00"),
                    startDate=_strToSqlDateTime("2019-11-01 19:00:00"),
                    limit=300,
                    offset=0,
                    tagmode="any")

            # print(m.last_request.qs)

            self.assertEqual(
                m.last_request.qs,
                {'where': ['{"recordingdatetime": {"$gte": "2019-11-01t19:00:00", "$lte": "2019-11-06t06:30:00"}}'], 'limit': ['300'], 'offset': ['0'], 'tagmode': ['any']}
            )

    def test_get_valid_recordingId(self):
        """Test CacophonyClient.get with a valid recording_id from mocked CacophonyServer object."""
        #TODO: handle error as correct result
        int_recording_id = 432109
        str_recording_id = '432109'
        mock_json_result = {'key1': 'value1', 'key2': 'value2'}
        with requests_mock.Mocker() as m:
            m.register_uri(
                requests_mock.GET,
                "{apiURL}/api/v1/recordings/{recording_id}".format(apiURL=defaults["apiURL"],
                                                            recording_id=str(int_recording_id)),
                json={"recording":mock_json_result}, status_code=200
            )
            result = self.cli.get(int_recording_id)

            # print(m.last_request.qs)
            self.assertEqual(result, mock_json_result)
            self.assertEqual(m.last_request.qs, {})
            self.assertEqual(m.last_request.path, 
                            '/api/v1/recordings/{str_recording_id}'.format(
                                str_recording_id=str_recording_id))

    def test_get_invalid_recordingId(self):
        """Test CacophonyClient.get with an invalid recording_id from mocked CacophonyServer object."""
        int_recording_id = ''
        str_recording_id = ''
        mock_json_result = "some sort of error message"
        #Check What Exception we get
        result=None
        #TODO: change this the valid exception
        with self.assertRaises(Exception) as context:

            # Setup expected request
            with requests_mock.Mocker() as m:
                m.register_uri(
                    requests_mock.GET,
                    "{apiURL}/api/v1/recordings/{recording_id}".format(apiURL=defaults["apiURL"],
                                                                recording_id=str(int_recording_id)),
                    json={"message":mock_json_result}, status_code=400
                )
                # TEST 
                result = self.cli.get(int_recording_id)
            
        self.assertTrue(type(context.exception)==OSError)
        self.assertTrue('request failed (400): '+mock_json_result in str(context.exception))
        #TODO: check what exception was raised
        # print("This exception raised:{}".format(context.exception))

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

# if __name__ == '__main__':
#     import nose2
#     nose2.main(verbosity=2)

if __name__ == '__main__':
    unittest.main()