import requests
import json

# URL of CertStream's latest.json endpoint
URL = "https://certstream.calidog.io/latest.json"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()  # Raises an error for bad HTTP status codes

    data = response.json()  # Parse JSON response
    print(json.dumps(data, indent=2))  # Pretty-print the JSON

except requests.exceptions.HTTPError as errh:
    print("HTTP error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Connection error:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout error:", errt)
except requests.exceptions.RequestException as err:
    print("Request error:", err)
