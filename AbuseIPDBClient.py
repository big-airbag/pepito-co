def AbuseIPDBClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        raise NotImplementedError

    def check_reputation(self, ip: str | None, domain: str | None):
        raise NotImplementedError
