import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from proxy_utils import find_working_proxy

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

username = os.getenv("LT_USERNAME")
access_key = os.getenv("LT_ACCESS_KEY")

# LambdaTest Hub URL
grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

# Define the target URL
test_url = "http://books.toscrape.com/catalogue/the-book-of-basketball-the-nba-according-to-the-sports-guy_232/index.html"

# 1. Get a working proxy
working_proxy = find_working_proxy(test_url)
if not working_proxy:
    print("❌ No working proxy found.")
    exit()

# 2. Set desired capabilities for LambdaTest
options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server=http://{working_proxy}')
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('--headless=new')

lt_capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest", 
    "platformName": "Windows 11",
    "seCdp": True,
    "LT:Options": {
        "username": username,
        "accessKey": access_key,
        "build": "Selenium Proxy Python tests",
        "project": "Running Proxy Scripts",
        "name": "Book Scrape Test with Proxy",
        "selenium_version": "4.19.0", 
        "w3c": True,
        "visual": True,
        "video": True,
    },
}

for key, value in lt_capabilities.items():
    options.set_capability(key, value)

# 3. Create Remote WebDriver session
try:
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    driver.get(test_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#content_inner"))
    )

    # Scrape details
    name = driver.find_element(By.CSS_SELECTOR, "#content_inner h1").text.strip()
    price = driver.find_element(By.CSS_SELECTOR, ".product_main .price_color").text.strip()
    stock = driver.find_element(By.CSS_SELECTOR, ".instock.availability").text.strip()

    print(f"\n✅ Scraped using proxy: {working_proxy}\n")
    print(f"🔹 Product : {name}")
    print(f"🔹 Price   : {price}")
    print(f"🔹 Stock   : {stock}")

except Exception as e:
    print(f"❌ Error during scraping: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
