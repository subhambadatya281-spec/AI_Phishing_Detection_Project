from urllib.parse import urlparse
import re

def extract_features(url):

    parsed = urlparse(url)

    hostname = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {}

    features["NumDots"] = url.count(".")
    features["SubdomainLevel"] = max(0, hostname.count(".") - 1)
    features["PathLevel"] = path.count("/")
    features["UrlLength"] = len(url)
    features["NumDash"] = url.count("-")
    features["AtSymbol"] = 1 if "@" in url else 0
    features["NumUnderscore"] = url.count("_")
    features["NumPercent"] = url.count("%")
    features["NumQueryComponents"] = query.count("&") + 1 if query else 0
    features["NumHash"] = url.count("#")

    features["NumNumericChars"] = len(
        re.findall(r"\d", url)
    )

    features["NoHttps"] = 0 if url.startswith("https://") else 1

    features["HostnameLength"] = len(hostname)
    features["PathLength"] = len(path)
    features["QueryLength"] = len(query)

    return features


url = input("Enter URL: ")

print(extract_features(url))