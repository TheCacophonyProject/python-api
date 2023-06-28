from .apibase import APIBase

import json
import requests
from urllib.parse import urljoin
from requests_toolbelt.multipart.encoder import MultipartEncoder


class DeviceAPI(APIBase):
    def __init__(self, baseurl, devicename, password="password"):
        super().__init__(baseurl, devicename, password, "device")

    def upload_recording(self, filename, jsonProps=None, timeout=200):
        url = urljoin(self._baseurl, "/api/v1/recordings")

        if jsonProps is None:
            jsonProps = '{"type": "thermalRaw"}'
            print(" null props")

        with open(filename, "rb") as thermalfile:
            multipart_data = MultipartEncoder(
                fields={"file": ("file.py", thermalfile), "data": jsonProps}
            )
            headers = {
                "Content-Type": multipart_data.content_type,
                "Authorization": self._token,
            }
            r = requests.post(
                url, data=multipart_data, headers=headers, timeout=timeout
            )

        if r.status_code == 200:
            print("Successful upload of ", filename)

        self._check_response(r)
        return r.json()
