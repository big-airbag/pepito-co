from BaseClient import BaseClient
import pytest

def test_create_BaseClient():
    BaseClient("http://myurl.com")
    with pytest.raises(Exception):
        BaseClient("myurl")
    BaseClient(base_url="http://myurl.com", headers={})
    with pytest.raises(Exception):
        BaseClient(base_url="http://myurl.com", headers=3)