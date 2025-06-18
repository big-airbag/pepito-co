import requests
import validators


class BaseApiClient:
    """
    A Base Api Client
    """

    def __init__(self, base_url: str, headers: dict | None = None):
        """Initialize the client with given base_url and headers

        Args:
            base_url (str): The base URL of the API
            headers (dict | None, optional): Some headers. Defaults to None.
        """
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
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value: dict | None = None):
        if not isinstance(value, dict) and value is not None:
            raise TypeError("Headers must be a dict or None")
        self._headers = value or {}

    def endpoint_request(
        self,
        endpoint: str,
        method: str,
        json_body: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
        verify_ssl: bool = False,
    ) -> requests.Response:
        """Request an API endpoint

        Args:
            endpoint (str): API endpoint
            method (str): HTTP method
            json_body (dict | None, optional): JSON payload. Defaults to None.
            headers (dict | None, optional): Headers. Defaults to None.
            params (dict | None, optional): Query parameters. Defaults to None.
            verify_ssl (bool, optional): SSL verification. Defaults to False.

        Returns:
            requests.Response: HTTP Response
        """
        headers = headers | self._headers if headers is not None else self._headers

        response = requests.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            json=json_body,
            params=params,
            headers=headers,
            verify=verify_ssl,
        )
        return response
