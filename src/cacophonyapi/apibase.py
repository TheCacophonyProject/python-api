import json
import requests
from urllib.parse import urljoin


class APIBase:
    def __init__(self, baseurl, loginname, password, logintype):
        self._baseurl = baseurl
        self._loginname = loginname
        self._token = self._get_jwt(password, logintype)
        self._auth_header = {"Authorization": self._token}

    def _get_jwt(self, password, logintype):
        url = urljoin(self._baseurl, "/authenticate_" + logintype)
        if logintype == "user":
            r = requests.post(
                url, data={"email": self._loginname, "password": password}
            )
        else:
            nameProp = logintype + "name"
            r = requests.post(
                url, data={nameProp: self._loginname, "password": password}
            )

        if r.status_code == 200:
            return r.json().get("token")
        elif r.status_code == 422:
            raise ValueError(
                "Could not log on as '{}'.  Please check {} name.".format(
                    self._loginname, logintype
                )
            )
        elif r.status_code == 401:
            raise ValueError(
                "Could not log on as '{}'.  Please check password.".format(
                    self._loginname
                )
            )
        else:
            r.raise_for_status()

    def _check_response(self, r):
        if r.status_code in (400, 422):
            j = r.json()
            messages = j.get("messages", j.get("message", ""))
            raise IOError("request failed ({}): {}".format(r.status_code, messages))
        r.raise_for_status()
        return r.json()
