from BaseClient import BaseClient
import json
import socket
import requests

class AbuseIPDBClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(base_url="https://api.abuseipdb.com/api/v2",headers={
            "Accept":"application/json",
            "Key": api_key
        })
        self.api_key = api_key
        
        #TODO: when api key is set, set headers

    #TODO: typing
    def check_reputation(self, ip: str | None = None, domain: str | None = None):
        if ip is None and domain is None:
            raise ValueError("Provide IP or domain")
        if ip is None:
            ip = socket.gethostbyname(domain)
        url = "{}/check?ipAddress={}".format(self.base_url, requests.utils.quote(ip))
        response = requests.get(url=url, headers=self.headers)

        if response.status_code != 200:
            raise Exception("{} response AbuseIPDB API", response.status_code)
        return response.json()["data"]["abuseConfidenceScore"]
