from BaseApiClient import BaseApiClient
import socket
import requests


class AbuseIPDBClient(BaseApiClient):
    """
    A Client for AbuseIPDB API
    """
    def __init__(self, api_key: str):
        """Initialize the client with given API Key

        Args:
            api_key (str): AbuseIPDB API key
        """
        super().__init__(base_url="https://api.abuseipdb.com/api/v2", headers={"Key": api_key})
        self.api_key = api_key

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        assert type(value) == str, "api_key must be a str"
        self._api_key = value

    def check_reputation(self, ip: str | None = None, domain: str | None = None) -> int:
        """Check domain reputation on AbuseIPDB
        If both IP and domain are provided, uses domain.
        Args:
            ip (str | None, optional): IP address. Defaults to None.
            domain (str | None, optional): A domain. Defaults to None.

        Raises:
            ValueError: If both arguments are None
            Exception: HTTP error

        Returns:
            int: AbuseIPDB confidence score
        """
        endpoint = "/check"

        if ip is None and domain is None:
            raise ValueError("Provide IP or domain")
        if domain is not None:
            ip = socket.gethostbyname(domain)

        response = self.endpoint_request(
            endpoint=endpoint,
            method="GET",
            params={"ipAddress": requests.utils.quote(ip)},
            headers={"Accept": "application/json"},
        )
        if response.status_code != 200:
            raise Exception("{} response AbuseIPDB API".format(response.status_code))
        return response.json()["data"]["abuseConfidenceScore"]
