import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_html_features(url):

    features = {
        "PctExtHyperlinks": 0,
        "IframeOrFrame": 0,
        "MissingTitle": 0,
        "InsecureForms": 0,
        "SubmitInfoToEmail": 0
    }

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Missing Title
        if soup.title is None:
            features["MissingTitle"] = 1

        # Iframe Detection
        if soup.find("iframe"):
            features["IframeOrFrame"] = 1

        # External Links %
        links = soup.find_all("a", href=True)

        if len(links) > 0:
            ext_count = 0

            domain = urlparse(url).netloc

            for link in links:
                href = link["href"]

                if href.startswith("http"):
                    if domain not in href:
                        ext_count += 1

            features["PctExtHyperlinks"] = (
                ext_count / len(links)
            ) * 100

        # Forms
        forms = soup.find_all("form")

        for form in forms:

            action = form.get("action", "")

            if action.startswith("http"):
                if urlparse(url).netloc not in action:
                    features["InsecureForms"] = 1

            if "mailto:" in action:
                features["SubmitInfoToEmail"] = 1

    except Exception as e:
        print("Error:", e)

    return features


url = input("Enter URL: ")

result = extract_html_features(url)

print("\nHTML Features:\n")

for k, v in result.items():
    print(f"{k}: {v}")
    