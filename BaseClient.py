import requests
import validators

#TODO: Typing

class BaseClient(object):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, value:str):
        print(value)
        assert validators.url(value), "BaseClient base_url attribute is malformed."
        self._base_url = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if not isinstance(value, dict) and value is not None:
            raise TypeError("Headers must be a dict or None")
        self._headers = value or {}
        

    def http_request(
        self, method: str, json_body=None, headers=None, verify_ssl= False
    ) :
        method = method.upper()
        if method not in ["GET", "POST"]:
            raise NotImplementedError
        
        #TODO: rewrite
        if headers is not None:
            headers = headers|self._headers
        else:
            headers = self._headers
        if method == "GET":
            response = requests.get(self.base_url, json=json_body, headers=headers, verify=verify_ssl)
        else:
            response = requests.post(self.base_url, json=json_body, headers=headers, verify=verify_ssl)
       
        return response