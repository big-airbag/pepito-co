import json
from unittest.mock import patch
import pytest
from AbuseIPDBClient import AbuseIPDBClient

def test_create_AbuseIPDBClient():
    aipc = AbuseIPDBClient("mykey")
    assert aipc.base_url == "https://api.abuseipdb.com/api/v2"
    assert "Key" in aipc.headers


def test_check_reputation_AbuseIPDBClient():
    aipc = AbuseIPDBClient("mykey")
    mock_response = """{
        "data": {
            "ipAddress": "45.134.26.79",
            "isPublic": true,
            "ipVersion": 4,
            "isWhitelisted": false,
            "abuseConfidenceScore": 100,
            "countryCode": "RU",
            "usageType": "Data Center/Web Hosting/Transit",
            "isp": "Proton66 LLC",
            "domain": "proton66.ru",
            "hostnames": [],
            "isTor": false,
            "totalReports": 52019,
            "numDistinctUsers": 233,
            "lastReportedAt": "2025-06-17T12:36:09+00:00"
        }
    }"""
    with patch("requests.request") as mock_request:
        mock_request.return_value.json.return_value = json.loads(mock_response)
        mock_request.return_value.status_code = 200
        score = aipc.check_reputation(ip="45.134.26.79")
        assert score == 100

        score = aipc.check_reputation(domain="localhost")
        assert score == 100

        with pytest.raises(Exception):
            aipc.check_reputation()

        mock_request.return_value.status_code = 403
        with pytest.raises(Exception):
            aipc.check_reputation(ip="45.134.26.79")

        