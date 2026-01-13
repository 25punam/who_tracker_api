# api/services/who_client.py
import requests

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_first_100():
    params = {
    "startIndex": 0,
    "resultsPerPage": 100
  }

    response = requests.get(BASE_URL, timeout=15, params=params)
    response.raise_for_status()
    return response.json()
