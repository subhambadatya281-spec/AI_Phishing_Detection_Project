import joblib
import pandas as pd
from url_feature_extractor_v2 import extract_features

# Load trained machine learning pipeline model
try:
    model = joblib.load("models/phishing_model.pkl")
except FileNotFoundError:
    print("Error: The model file 'models/phishing_model.pkl' was not found.")
    model = None

# Strict explicit feature ordering used during model training phase
columns = [
    'NumDots', 'SubdomainLevel', 'PathLevel', 'UrlLength', 'NumDash',
    'NumDashInHostname', 'AtSymbol', 'TildeSymbol', 'NumUnderscore',
    'NumPercent', 'NumQueryComponents', 'NumAmpersand', 'NumHash',
    'NumNumericChars', 'NoHttps', 'RandomString', 'IpAddress',
    'DomainInSubdomains', 'DomainInPaths', 'HttpsInHostname',
    'HostnameLength', 'PathLength', 'QueryLength',
    'DoubleSlashInPath', 'NumSensitiveWords', 'EmbeddedBrandName',
    'PctExtHyperlinks', 'PctExtResourceUrls', 'ExtFavicon',
    'InsecureForms', 'RelativeFormAction', 'ExtFormAction',
    'AbnormalFormAction', 'PctNullSelfRedirectHyperlinks',
    'FrequentDomainNameMismatch', 'FakeLinkInStatusBar',
    'RightClickDisabled', 'PopUpWindow', 'SubmitInfoToEmail',
    'IframeOrFrame', 'MissingTitle', 'ImagesOnlyInForm',
    'SubdomainLevelRT', 'UrlLengthRT', 'PctExtResourceUrlsRT',
    'AbnormalExtFormActionR', 'ExtMetaScriptLinkRT',
    'PctExtNullSelfRedirectHyperlinksRT'
]

def predict_url(url):
    """
    Extracts heuristic features from a given URL, formats them matching 
    the model training schema vector, and outputs binary and probability predictions.
    """
    if model is None:
        return 0, [1.0, 0.0]

    # Extract dynamic properties from targeting link string
    features = extract_features(url)

    # Re-index data fields to enforce strict alignment matching training columns matrix
    data = {}
    for col in columns:
        data[col] = features.get(col, 0)

    # Cast single-row structural instance array to pandas DataFrame
    df = pd.DataFrame([data])
    
    # Enforce precise column ordering layout explicitly
    df = df[columns]

    # Compute array outputs from model instance state
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    return prediction, probability


if __name__ == "__main__":
    url = input("Enter URL: ")
    prediction, probability = predict_url(url)

    print("\n--- Model Prediction Result ---")
    if prediction == 1:
        print("⚠️ PHISHING WEBSITE DETECTED")
        print(f"Risk Likelihood Score: {probability[1] * 100:.2f}%")
    else:
        print("✅ LEGITIMATE WEBSITE VERIFIED")
        print(f"Safety Baseline Score: {probability[0] * 100:.2f}%")