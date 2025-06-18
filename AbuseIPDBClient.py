from BaseApiClient import BaseApiClient
import json
import socket
import requests


class AbuseIPDBClient(BaseApiClient):
    def __init__(self, api_key: str):
        super().__init__(base_url="https://api.abuseipdb.com/api/v2", headers={"Key": api_key})
        self.api_key = api_key

    @property
    def api_key(self) ->str:
        return self._api_key
    
    @api_key.setter
    def api_key(self, value:str):
        assert type(value) == str, "api_key must be a str"
        self._api_key = value


    # TODO: typing
    def check_reputation(self, ip: str | None = None, domain: str | None = None):
        endpoint = "/check"

        if ip is None and domain is None:
            raise ValueError("Provide IP or domain")
        if ip is None:
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
