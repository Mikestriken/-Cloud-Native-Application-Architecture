import requests

def fetch_ip() -> str:
    """Fetches your public IP address from an HTTP API."""
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]