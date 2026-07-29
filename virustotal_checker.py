import requests
import time

API_KEY = "44674be43dcbf386cc16f5096e83259bc826320ebc26a2cbfeacbf0fd797a98d"

def check_virustotal(url):

    headers = {
        "x-apikey": API_KEY
    }

    try:

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=20
        )

        if response.status_code != 200:
            return f"API Error: {response.status_code}"

        analysis_id = response.json()["data"]["id"]

        time.sleep(5)

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=20
        )

        if report.status_code != 200:
            return f"Report Error: {report.status_code}"

        stats = report.json()["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)

        return f"Malicious: {malicious} | Suspicious: {suspicious} | Harmless: {harmless}"

    except Exception as e:
        return str(e)