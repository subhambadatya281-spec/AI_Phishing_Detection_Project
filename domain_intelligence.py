import socket
import requests
from urllib.parse import urlparse

def get_domain_info(url):
    """
    Resolves the live domain string into a public IPv4 network address and 
    queries dynamic GeoIP nodes to fetch Country, Location, and ISP metrics.
    """
    try:
        # Step 1: Isolate the clean hostname from the complete URL scheme string
        domain = urlparse(url).netloc.lower()
        if not domain:
            domain = urlparse(f"https://{url}").netloc.lower()
    except Exception:
        return {
            "Domain": "Unknown", "IP": "Not Available", "Country": "Not Available",
            "Region": "Not Available", "City": "Not Available", "ISP": "Not Available"
        }

    if domain.startswith("www."):
        domain = domain[4:]

    # Strip network port numbers if present on the connection string stream
    domain = domain.split(':')[0]

    # --- Step 2: Extract Live Public IPv4 Address ---
    try:
        ip = socket.gethostbyname(domain)
    except Exception as dns_error:
        print(f"[DNS Exception] Hostname lookup failed for {domain}: {dns_error}")
        ip = "Not Available"

    # --- Step 3: Core GeoIP and ISP Extraction Engine ---
    # Default values ensure your risk engine functions smoothly if network drops occur
    fallback_data = {
        "Domain": domain,
        "IP": ip,
        "Country": "Not Available",
        "Region": "Not Available",
        "City": "Not Available",
        "ISP": "Not Available"
    }

    if ip == "Not Available":
        return fallback_data

    try:
        # Access highly stable open geo-location query infrastructure
        api_url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp"
        response = requests.get(api_url, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "Domain": domain,
                    "IP": ip,
                    "Country": data.get("country", "Not Available"),
                    "Region": data.get("regionName", "Not Available"),
                    "City": data.get("city", "Not Available"),
                    "ISP": data.get("isp", "Not Available")
                }
    except Exception as api_err:
        print(f"[API Network Drop] GeoIP infrastructure timed out for IP {ip}: {api_err}")

    return fallback_data

if __name__ == "__main__":
    print("--- Central Infrastructure GeoIP Locator Active ---")
    target_link = input("Provide destination link for validation: ")
    results = get_domain_info(target_link)
    
    print("\n--- Structural Network Records Discovered ---")
    for key, value in results.items():
        print(f"{key}: {value}")