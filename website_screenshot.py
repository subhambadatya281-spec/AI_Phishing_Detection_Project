import os
import requests

def capture_screenshot(url):
    """
    Captures a screenshot of the specified URL and saves it to static/website.png.
    Uses an external rendering API to remain compatible with cloud environments
    where Google Chrome / Selenium binaries are unavailable.
    """
    try:
        # Ensure static folder exists
        os.makedirs("static", exist_ok=True)
        save_path = os.path.join("static", "website.png")

        # Screenshot API service
        api_url = f"https://image.thum.io/get/width/1200/crop/800/{url}"
        
        response = requests.get(api_url, timeout=12)
        
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        
        print(f"Failed to retrieve screenshot. HTTP Status Code: {response.status_code}")
        return False

    except Exception as e:
        print(f"Screenshot Generation Error: {e}")
        return False
