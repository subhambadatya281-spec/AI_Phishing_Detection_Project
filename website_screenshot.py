from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import os

def capture_screenshot(url):

    driver = None

    try:

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            )
        )

        driver.set_page_load_timeout(10)

        driver.get(url)

        os.makedirs("static", exist_ok=True)

        driver.save_screenshot(
            "static/website.png"
        )

        return True

    except WebDriverException:
        return False

    except Exception:
        return False

    finally:
        if driver:
            driver.quit()