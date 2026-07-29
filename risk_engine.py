from urllib.parse import urlparse
from brand_detector import detect_brand
from ssl_checker import check_ssl
from domain_age import get_domain_age
from domain_intelligence import get_domain_info

print("UNIVERSAL_RISK_ENGINE_PRODUCTION_READY")

def calculate_risk(url, prediction, ocr_text=""):
    """
    Evaluates cumulative risk indices across predictive and heuristic layers.
    Gracefully handles network drops to eliminate false positive penalties on safe sites.
    """
    risk = 0
    reasons = []

    try:
        hostname = urlparse(url).netloc.lower()
    except Exception:
        return 100, ["Malformed URL structure input"]

    if hostname.startswith("www."):
        hostname = hostname[4:]

    # 1. Machine Learning Predictive Model Evaluation
    if prediction == 1:
        risk += 50
        reasons.append("ML model detected algorithmic phishing signatures")
    
    # 2. Advanced Heuristic Identity Analysis (Brand Spoofing Detection)
    brands = detect_brand(url)

    # Trusted anchor array to bypass structural false positives
    official_brand_anchors = [
        "google.com", "google.co.in", "gmail.com", "paypal.com", "amazon.com", 
        "amazon.in", "facebook.com", "instagram.com", "microsoft.com", "apple.com",
        "netflix.com", "twitter.com", "linkedin.com", "yahoo.com", "onlinesbi.sbi", 
        "sbi.co.in", "uidai.gov.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
        "steamcommunity.com", "steampowered.com", "wikipedia.org", "github.com"
    ]

    is_official_anchor = False
    for anchor in official_brand_anchors:
        if hostname == anchor or hostname.endswith("." + anchor):
            is_official_anchor = True
            break

    # Apply impersonation penalties ONLY if the asset is not an official whitelisted anchor
    if brands and not is_official_anchor:
        risk += 35
        reasons.append("Critical Alert: Brand name structural impersonation detected")

    for detected in brands:
        if "typosquatting suspected" in str(detected).lower():
            risk += 25
            reasons.append("Critical Alert: Deceptive typosquatting character mutation caught")
            break

    # 3. Structural Segment Check (Government & Financial Keyphrases)
    untrusted_indicators = {
        "government": (["gov", "government", "uidai", "aadhaar", "passport", "visa"], [".gov.in", ".nic.in"], 40, "Unauthorized government identity reference"),
        "banking": (["bank", "secure-login", "wallet", "crypto", "checkout", "sbi", "hdfc", "icici"], [".bank", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com"], 35, "Potential financial infrastructure spoofing"),
        "account_actions": (["login", "verify", "verification", "security", "update", "signin", "password-reset"], [], 15, "Suspicious urgency call-to-action keyword in URL path")
    }

    for sector, (keywords, exceptions, penalty, log_msg) in untrusted_indicators.items():
        if any(word in hostname for word in keywords):
            if not any(ex in hostname for ex in exceptions) and not is_official_anchor:
                risk += penalty
                reasons.append(log_msg)

    # 4. Global Untrusted Infrastructure Targets (TLD Profiling)
    dangerous_tlds = [".xyz", ".top", ".click", ".site", ".shop", ".online", ".club", ".work", ".info", ".live"]
    for tld in dangerous_tlds:
        if hostname.endswith(tld):
            risk += 20
            reasons.append(f"Untrusted infrastructure TLD target identified: {tld}")
            break

    # 5. SSL Protocol Validation
    try:
        ssl_info = check_ssl(url)
        # Apply penalty ONLY if SSL is explicitly verified as False/Expired, not on connection timeouts
        if ssl_info and ssl_info.get("SSL") is False and not is_official_anchor:
            risk += 20
            reasons.append("Insecure transmission: Active SSL certificate validation failure")
    except Exception:
        pass  # Ignore network socket timeout drops

    if url.startswith("http://"):
        risk += 15
        reasons.append("Vulnerable protocol usage: Base HTTP deployed without transport encryption")

    # 6. Active Live Hostname Verification (DNS State Lookup)
    try:
        domain_info = get_domain_info(url)
        # Apply penalty only if the domain explicitly responds with NXDOMAIN (not found)
        if domain_info and domain_info.get("Domain") == "Unknown" and not is_official_anchor:
            risk += 45
            reasons.append("Network validation exception: Hostname failed active DNS resolution")
    except Exception:
        pass

    # 7. Lifespan Registration Heuristics (Domain Age Tracking)
    try:
        age_info = get_domain_age(url)
        age_days = age_info.get("Age Days")
        if isinstance(age_days, int):
            if age_days < 30 and not is_official_anchor:
                risk += 35
                reasons.append(f"Highly volatile threat window: Domain lifespan is exceptionally new ({age_days} days)")
            elif age_days < 180 and not is_official_anchor:
                risk += 15
                reasons.append(f"Provisional trust window: Domain lifespan is less than 6 months ({age_days} days)")
    except Exception:
        pass

    # 8. CRITICAL OVERRIDE PREVALENCE
    # Forces high-confidence phishing indicators to trigger blockages despite older age stamps.
    if brands and not is_official_anchor:
        if risk < 85:
            risk = 85
            reasons.append("Threat Matrix Override: Brand spoofing signatures take precedence over domain age metrics")

    # 9. Clear Out Safe Defaults
    # If it is an official trusted anchor or matches no threats, force risk down to zero.
    if is_official_anchor or len(reasons) == 0:
        risk = 0
        reasons = ["No active risk signatures matched"]

    if risk > 100:
        risk = 100

    return risk, reasons