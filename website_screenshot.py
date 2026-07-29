import os
import requests

def capture_screenshot(url):
    try:
        # Output directory ensure karein
        os.makedirs("static", exist_ok=True)
        save_path = "static/website.png"

        # Free Screenshot API Endpoint
        api_url = f"https://image.thum.io/get/width/1200/crop/800/{url}"
        
        response = requests.get(api_url, timeout=12)
        
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        
        return False

    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        return False
