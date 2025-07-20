import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from proxy_utils import find_working_proxy 

# Define the target URL (can vary per script)
test_url = "http://books.toscrape.com/catalogue/the-book-of-basketball-the-nba-according-to-the-sports-guy_232/index.html"

# Get a healthy proxy
working_proxy = find_working_proxy(test_url)
if not working_proxy:
    print("❌ No working proxy found.")
    exit()

# Set up Selenium with working proxy
options = Options()
options.add_argument(f'--proxy-server=http://{working_proxy}')
options.add_argument('--headless=new')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ----- 4. Open Target Page -----
driver.get(test_url)
time.sleep(3)

try:
    wait = WebDriverWait(driver, 10)

    # 4. Scrape Details
    name = driver.find_element(By.CSS_SELECTOR, "#content_inner h1").text.strip()
    price = driver.find_element(By.CSS_SELECTOR, "#content_inner .product_main .price_color").text.strip()
    stock = driver.find_element(By.CSS_SELECTOR, "#content_inner .product_main .instock.availability").text.strip()
    rating = driver.find_element(By.CSS_SELECTOR, "#product_gallery .item.active img").get_attribute("value")

    # 5. Output
    print(f"\n✅ Scraped using proxy: {working_proxy}\n")
    print(f"🔹 Product : {name}")
    print(f"🔹 Price   : {price}")
    print(f"🔹 Stock   : {stock}")
    print(f"🔹 Rating  : {rating}")

except Exception as e:
    print(f"❌ Timed out loading the page: {e}")
except Exception as e:
    print(f"❌ Error during scraping: {e}")
finally:
    driver.quit()
