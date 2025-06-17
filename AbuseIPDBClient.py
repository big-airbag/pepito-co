from BaseApiClient import BaseApiClient
import json
import socket
import requests


class AbuseIPDBClient(BaseApiClient):
    def __init__(self, api_key: str):
        super().__init__(base_url="https://api.abuseipdb.com/api/v2", headers={"Key": api_key})
        self._api_key = api_key

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
