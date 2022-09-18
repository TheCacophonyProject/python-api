# -*- coding: utf-8 -*-

"""Unit tests for the Python client of the  Cacophony Project REST API server.
NB/WARNING:
This module implements tests for the UserAPI class
but does so
 + WITH a server instance running
 + by mocking all the expected responses.
So any change of (response format from) the server **COULD ** be
detected by this module.
See client_test.py for tests WITHOUT a running server instance.
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

import os
from cacophonyapi.user import UserAPI


defaults = {
    "apiURL": "http://localhost:1080",
    "defaultDevice": "test-device",
    "defaultPassword": "test-password",
    "defaultGroup": "test-group",
    "defaultGroup2": "test-group-2",
    "defaultUsername": "cacophony-client@email.com",
    "defaultuserPassword": "test-user-password",
    "filesURL": "/files",
    "hostsFileString": "`127.0.0.1 raspberrypi::1 localhost",
}
# TODO: test a more complex password


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
        assert method == kwargs.get("method", "GET")

        if method == "POST":
            data = kwargs.get("data", None)

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

    return mock.patch.object(cli._session, "request", side_effect=request)


class liveTESTcacophonyapi(unittest.TestCase):
    """Set up the TestCacophonyClient object."""

    def setUp(self):
        """Initialize an instance of TestInfluxDBClient object."""
        # By default, raise exceptions on warnings
        warnings.simplefilter("error", FutureWarning)

        self.cli = UserAPI(
            baseurl=defaults["apiURL"],
            username=defaults["defaultUsername"],
            password=defaults["defaultuserPassword"],
        )

    def test_scheme(self):
        """Set up the test schema for TestCacophonyClient object."""
        cli = UserAPI(
            baseurl=defaults["apiURL"],
            username=defaults["defaultUsername"],
            password=defaults["defaultuserPassword"],
        )
        self.assertEqual(defaults["apiURL"], cli._baseurl)

    def test_upload_recording(self):
        """Test UserAPI.upload_recordings ( parameters passed: groupname, devicename, filename, props) to mocked CacophonyServer object.
        Default test user is read only so should fail with permission error"""
        testcases = [
            {
                "filename": os.path.join(os.path.dirname(__file__), "test1.cptv"),
                "mock_file.side_effect": None,
                "devicename": "test-device",
                "groupname": "test-group",
                "prop": None,
                "expectedProp": {"type": "thermalRaw"},
                "expectedResult": {
                    "outcome": "failureHTTPforbidden",
                    "validator": lambda test: test,
                },
                "mockRequestStatusCode": 403,
            },
        ]
        for tc in testcases:
            print(tc)
            if tc["expectedResult"]["outcome"] == "success":
                # ----------------------- API call UNDERTEST ------------------
                result = self.cli.upload_recording(
                    tc["groupname"], tc["devicename"], tc["filename"], tc["prop"]
                )
                # ----------------------------------------------------------------
                print(result)
                self.assertTrue(result["success"])

            elif tc["expectedResult"]["outcome"] == "failureHTTPforbidden":
                try:
                    with self.assertRaises(requests.HTTPError):
                        # ----------------------- API call UNDERTEST ------------------
                        result = self.cli.upload_recording(
                            tc["groupname"],
                            tc["devicename"],
                            tc["filename"],
                            tc["prop"],
                        )
                    # ----------------------------------------------------------------
                    print(self)
                    # TODO: check the message returned
                    # self.assertTrue(result['success'])
                except Exception as e:
                    self.fail("Unknown Exception_instance={})".format(e))
            else:
                # TODO: Check the mockrequest was called, and mockfile
                self.assertTrue(
                    False, "Something not being checked ----------------------------"
                )


if __name__ == "__main__":
    unittest.main()

"""
	goconfig "github.com/TheCacophonyProject/go-config"
	"github.com/TheCacophonyProject/go-config/configtest"
	"github.com/spf13/afero"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)
"""
# tests against cacophony-api require apiURL to be pointing
# to a valid cacophony-api server and test-seed.sql to be run

# TODO: extend the testing in line with the GO-API
"""
rawFileSize = 100

responseHeader = http.StatusOK
rawThermalData = randString(100)
rawFileData = randString(rawFileSize)
testEventDetail = {"description": {"type": "test-id", "details": {"tail":"fuzzy"} } }

def TestNewTokenHttpRequest(t *testing.T) {
	ts := GetNewAuthenticateServer(t)
	defer ts.Close()

	api := getAPI(ts.URL, "", true)
	err := api.authenticate()
	assert.NoError(t, err)
}

func TestUploadThermalRawHttpRequest(t *testing.T) {
	ts := GetUploadThermalRawServer(t)
	defer ts.Close()

	api := getAPI(ts.URL, "", true)
	reader := strings.NewReader(rawThermalData)
	err := api.UploadThermalRaw(reader)
	assert.NoError(t, err)
}

func getTokenResponse() *tokenResponse {
	return &tokenResponse{
		Messages: []string{},
		Token:    "tok-" + randString(20),
		ID:       1,
	}
}

func getJSONRequestMap(r *http.Request) map[string]interface{} {
	var requestJson map[string]interface{}
	decoder := json.NewDecoder(r.Body)
	decoder.Decode(&requestJson)
	return requestJson
}

// GetRegisterServer returns a test server that checks that register posts contain
// password,group and devicename
func GetRegisterServer(t *testing.T) *httptest.Server {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestJson := getJSONRequestMap(r)

		assert.Equal(t, http.MethodPost, r.Method)
		assert.NotEmpty(t, requestJson["password"])
		assert.NotEmpty(t, requestJson["group"])
		assert.NotEmpty(t, requestJson["devicename"])

		w.WriteHeader(responseHeader)
		w.Header().Set("Content-Type", "application/json")
		token := getTokenResponse()
		json.NewEncoder(w).Encode(token)
	}))
	return ts
}

//GetNewAuthenticateServer returns a test server that checks that posts contains
// passowrd and devicename
func GetNewAuthenticateServer(t *testing.T) *httptest.Server {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestJson := getJSONRequestMap(r)

		assert.Equal(t, http.MethodPost, r.Method)
		assert.NotEmpty(t, requestJson["password"])
		assert.True(t, (requestJson["groupname"] != "" && requestJson["devicename"] != "") || requestJson["deviceID"] != "")

		w.WriteHeader(responseHeader)
		w.Header().Set("Content-Type", "application/json")
		token := getTokenResponse()
		json.NewEncoder(w).Encode(token)
	}))
	return ts
}

//getMimeParts retrieves data and  file:file and Value:data from a multipart request
func getMimeParts(r *http.Request) (string, string) {
	partReader, err := r.MultipartReader()

	var fileData, dataType string
	form, err := partReader.ReadForm(1000)
	if err != nil {
		return "", ""
	}

	if val, ok := form.File["file"]; ok {
		filePart := val[0]
		file, _ := filePart.Open()
		b := make([]byte, 1)
		for {
			n, err := file.Read(b)
			fileData += string(b[:n])
			if err == io.EOF {
				break
			}
		}
	}

	if val, ok := form.Value["data"]; ok {
		dataType = val[0]
	}
	return dataType, fileData
}

//GetUploadThermalRawServer checks that the message is multipart and contains the required multipartmime file:file and Value:data
//and Authorization header
func GetUploadThermalRawServer(t *testing.T) *httptest.Server {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		assert.Equal(t, http.MethodPost, r.Method)
		assert.NotEmpty(t, r.Header.Get("Authorization"))

		dataType, file := getMimeParts(r)
		assert.Equal(t, "{\"type\":\"thermalRaw\"}", dataType)
		assert.Equal(t, rawThermalData, file)

		w.WriteHeader(responseHeader)
	}))
	return ts
}

func TestAPIAuthenticate(t *testing.T) {
	api := getAPI(apiURL, defaultPassword, false)
	api.device.name = defaultDevice
	err := api.authenticate()
	assert.NoError(t, err)
	assert.NotEmpty(t, api.token)
}

func randomRegister() (*CacophonyAPI, error) {
	return Register(randString(20), randString(20), defaultGroup, apiURL)
}
"""
