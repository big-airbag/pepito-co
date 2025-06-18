import requests
import validators

# TODO: Typing


class BaseApiClient(object):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, value: str):
        assert type(value) == str, "BaseApiClient base_url must be a str"
        assert validators.url(value), "BaseApiClient base_url attribute is malformed."
        self._base_url = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if not isinstance(value, dict) and value is not None:
            raise TypeError("Headers must be a dict or None")
        self._headers = value or {}

    def endpoint_request(self, endpoint: str, method: str, json_body=None, headers=None, params=None, verify_ssl=False):
        # TODO: rewrite
        if headers is not None:
            headers = headers | self._headers
        else:
            headers = self._headers

        response = requests.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            json=json_body,
            params=params,
            headers=headers,
            verify=verify_ssl,
        )
        return response
