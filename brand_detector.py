import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

# Global target brand registry
SUSPICIOUS_BRANDS = [
    "paypal", "google", "amazon", "microsoft", "facebook", "instagram", 
    "netflix", "apple", "sbi", "hdfc", "icici", "axis", "uidai", "aadhaar",
    "twitter", "linkedin", "yahoo", "dropbox", "adobe", "bankofamerica", 
    "chase", "wellsfargo", "hsbc", "binance", "coinbase", "steam"
]

def similarity(a, b):
    """
    Computes sequence similarity ratio between strings.
    """
    return SequenceMatcher(None, a, b).ratio()

def normalize_domain(domain):
    """
    Translates visual look-alike characters back to standard alphabets.
    """
    replacements = {
        "0": "o", "1": "l", "3": "e", "4": "a", "5": "s", 
        "7": "t", "8": "b", "9": "g", "@": "a", "vv": "w", "rn": "m"
    }
    for old, new in replacements.items():
        domain = domain.replace(old, new)
    return domain

def detect_brand(url):
    """
    Intelligently extracts domain structures to evaluate brand spoofing 
    while preventing false positives on compound legitimate strings.
    """
    try:
        hostname = urlparse(url).netloc.lower()
    except Exception:
        return ["invalid url"]

    if hostname.startswith("www."):
        hostname = hostname[4:]

    # Step 1: Strip common top-level domain extensions to isolate the name core
    tld_extensions = r'\.(com|org|net|gov|edu|mil|co|in|uk|xyz|top|site|online|info|shop|click|club|work|live)$'
    clean_domain = re.sub(tld_extensions, '', hostname)

    # Step 2: Absolute Exact Match Validation
    for brand in SUSPICIOUS_BRANDS:
        if clean_domain == brand:
            return [brand]

    found_threats = []

    # Step 3: Comprehensive Security Evaluation Loop
    for brand in SUSPICIOUS_BRANDS:
        normalized_domain = normalize_domain(clean_domain)

        # Rule A: Character Swapping Matrix (e.g., g00gle.com, paypa1.com)
        if normalized_domain == brand and clean_domain != brand:
            found_threats.append(f"{brand} (typosquatting suspected)")
            continue

        # Rule B: Contextual Word Boundary Boundary Inspection
        if brand in normalized_domain:
            # PHISHING MARKER: Brand separated explicitly by special delimiters (e.g., steam-login, login.paypal)
            # COHESIVE LEGITIMATE WORD: Sub-component of a solid string (e.g., steamcommunity, microsoft)
            pattern = rf'(^|[\.\-]){brand}([\.\-]|$)'
            if re.search(pattern, normalized_domain):
                found_threats.append(f"{brand} (typosquatting suspected)")
                continue

        # Rule C: Fuzzy Length Proximity Matching (e.g., gooogle.com)
        if abs(len(clean_domain) - len(brand)) <= 3:
            score = similarity(normalized_domain, brand)
            if 0.85 <= score < 1.00 and clean_domain != brand:
                found_threats.append(f"{brand} (typosquatting suspected)")

    return list(set(found_threats))

if __name__ == "__main__":
    print("--- EVALUATING LEGITIMATE WEB CONTEXTS ---")
    print("https://google.com          ->", detect_brand("https://google.com"))          # Expected: ['google']
    print("https://steamcommunity.com  ->", detect_brand("https://steamcommunity.com"))  # Expected: [] (Safe)
    print("https://wikipedia.org       ->", detect_brand("https://wikipedia.org"))       # Expected: [] (Safe)

    print("\n--- EVALUATING MALICIOUS PHISHING LINKS ---")
    print("https://g00gle.com          ->", detect_brand("https://g00gle.com"))          # Expected: Flagged
    print("https://paypa1.com          ->", detect_brand("https://paypa1.com"))          # Expected: Flagged
    print("https://steam-login.xyz     ->", detect_brand("https://steam-login.xyz"))     # Expected: Flagged