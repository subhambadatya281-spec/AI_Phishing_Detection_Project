import requests
from urllib.parse import urlparse

def get_geoip(url):

    try:

        domain = urlparse(url).netloc

        response = requests.get(
            f"http://ip-api.com/json/{domain}"
        )

        data = response.json()

        return {
            "Country": data.get("country", "Unknown"),
            "Region": data.get("regionName", "Unknown"),
            "City": data.get("city", "Unknown"),
            "ISP": data.get("isp", "Unknown")
        }

    except Exception as e:

        print("GEOIP ERROR:", e)

        return {
            "Country": "Unknown",
            "Region": "Unknown",
            "City": "Unknown",
            "ISP": "Unknown"
        }