from BaseApiClient import BaseApiClient
import pytest


def test_create_BaseClient():
    BaseApiClient("http://myurl.com")
    with pytest.raises(Exception):
        BaseApiClient("myurl")
    BaseApiClient(base_url="http://myurl.com", headers={})
    with pytest.raises(Exception):
        BaseApiClient(base_url="http://myurl.com", headers=3)


def test_endpoint_request_BaseClient():
    bac = BaseApiClient("http://example.com", headers={"my_header": "my_header_value"})
    response = bac.endpoint_request(
        endpoint="/test", method="GET", json_body={"test": "valid"}, headers=None, params={"my_param": "my_value"}
    )
    assert response.request.url == "http://example.com/test?my_param=my_value"
    assert response.request.method == "GET"
    assert "my_header" in response.request.headers
    response = bac.endpoint_request(endpoint="/test", method="GET", headers={"param_header": "value"})
    assert "my_header" in response.request.headers
    assert "param_header" in response.request.headers
