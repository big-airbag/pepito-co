import requests


def BaseClient(object):
    def __init__(self, base_url: str, headers: dict = {}):
        raise NotImplementedError

    def http_request(
        self, method: str, json_body: dict, headers: dict = {}, verify_ssl: bool = False
    ):
        raise NotImplementedError
