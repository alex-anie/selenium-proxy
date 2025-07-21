import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from proxy_utils import find_working_proxy

# Load environment variables
load_dotenv()
username = os.getenv("LT_USERNAME")
access_key = os.getenv("LT_ACCESS_KEY")

# LambdaTest Hub URL
grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

# Target URL
test_url = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=40"

# Get a working proxy
working_proxy = find_working_proxy(test_url)
if not working_proxy:
    print("❌ No working proxy found.")
    exit()

# Configure Selenium + LambdaTest
options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server=http://{working_proxy}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless=new')

lt_capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest", 
    "platformName": "Windows 11",
    "seCdp": True,
    "LT:Options": {
        "username": username,
        "accessKey": access_key,
        "build": "Ecommerce Product Details",
        "project": "Product List",
        "name": "Get the product info",
        "selenium_version": "4.19.0", 
        "w3c": True,
        "visual": True,
        "video": True,
    },
}

for key, value in lt_capabilities.items():
    options.set_capability(key, value)

try:
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    driver.get(test_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#content_inner"))
    )

    # Wait for elements explicitly
    # name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#entry_216816 h1"))).text.strip()
    # price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#entry_216831 h3"))).text.strip()
    # stock = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#entry_216826 .badge-danger"))).text.strip()
    name = driver.find_element(By.CSS_SELECTOR, "#entry_216816 h1").text.strip()
    price = driver.find_element(By.CSS_SELECTOR, "#entry_216831 h3").text.strip()
    stock = driver.find_element(By.CSS_SELECTOR, "#entry_216826 .badge-danger").text.strip()


    # Output
    print(f"\n✅ Scraped using proxy: {working_proxy}")
    print(f"🔹 Product : {name}")
    print(f"🔹 Price   : {price}")
    print(f"🔹 Stock   : {stock}")

except Exception as e:
    print(f"❌ Error during scraping: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
