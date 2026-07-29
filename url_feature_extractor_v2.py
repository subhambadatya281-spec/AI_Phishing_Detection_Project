from urllib.parse import urlparse
import re

def is_ip_address(hostname):
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return 1 if re.match(ip_pattern, hostname) else 0

def extract_features(url):

    parsed = urlparse(url)

    hostname = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {}

    # Core URL Features
    features["NumDots"] = url.count(".")
    features["SubdomainLevel"] = max(0, hostname.count(".") - 1)
    features["PathLevel"] = path.count("/")
    features["UrlLength"] = len(url)

    features["NumDash"] = url.count("-")
    features["NumDashInHostname"] = hostname.count("-")

    features["AtSymbol"] = 1 if "@" in url else 0
    features["TildeSymbol"] = 1 if "~" in url else 0

    features["NumUnderscore"] = url.count("_")
    features["NumPercent"] = url.count("%")

    features["NumQueryComponents"] = (
        query.count("&") + 1 if query else 0
    )

    features["NumAmpersand"] = url.count("&")
    features["NumHash"] = url.count("#")

    features["NumNumericChars"] = len(
        re.findall(r"\d", url)
    )

    features["NoHttps"] = (
        0 if url.startswith("https://") else 1
    )

    features["IpAddress"] = is_ip_address(hostname)

    features["HostnameLength"] = len(hostname)
    features["PathLength"] = len(path)
    features["QueryLength"] = len(query)

    features["DoubleSlashInPath"] = (
        1 if "//" in path else 0
    )

    # Dataset me present additional features
    features["DomainInSubdomains"] = (
        1 if hostname.count(".") > 2 else 0
    )

    features["DomainInPaths"] = (
        1 if hostname in path else 0
    )

    features["HttpsInHostname"] = (
        1 if "https" in hostname.lower() else 0
    )

    features["RandomString"] = (
        1 if re.search(r"[a-zA-Z0-9]{20,}", hostname)
        else 0
    )

    return features

if __name__ == "__main__":

    url = input("Enter URL: ")

    result = extract_features(url)

    print("\nExtracted Features:\n")

    for k, v in result.items():
        print(f"{k}: {v}")