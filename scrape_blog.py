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
test_url = "https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/blog/home"

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

# ----- 5. Extract First Carousel Slides -----
all_cards = []

try:
    # ----- Wait until the first carousel appears -----
    wait = WebDriverWait(driver, 10)
    first_carousel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".swiper-wrapper")))

    # Now find the child slides inside the first carousel
    cards = first_carousel.find_elements(By.CLASS_NAME, "swiper-slide")

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, ".title a").text.strip()
            author = card.find_element(By.CSS_SELECTOR, ".author a").text.strip()
            comments = card.find_element(By.CSS_SELECTOR, ".comment").text.strip()
            views = card.find_element(By.CSS_SELECTOR, ".viewed").text.strip()

            all_cards.append({
                "title": title,
                "author": author,
                "comments": comments,
                "views": views
            })
        except Exception as e:
            print("⚠️ Error parsing card:", e)

except Exception as e:
    print(f"❌ Failed to locate carousel: {e}")

# ----- Output Results -----
print(f"\n✅ Scraped using proxy: {working_proxy}")
for i, card in enumerate(all_cards, 1):
    print(f"\nCard {i}:")
    print(f"  Title   : {card['title']}")
    print(f"  Author  : {card['author']}")
    print(f"  Comments: {card['comments']}")
    print(f"  Views   : {card['views']}")

# ----- Cleanup ----------------------------
driver.quit()

