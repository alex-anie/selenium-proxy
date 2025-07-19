import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ----- 1. Proxy Setup -----
proxy_list = [
"85.215.64.49:80",
"161.35.70.249:8080",
"139.59.1.14:80",
"113.160.132.195:8080",
"123.30.154.171:7777",
"8.211.194.78:1081",
"47.238.134.126:81",
"35.180.23.174:3128",
"133.18.234.13:80",
"219.65.73.81:80",
"114.6.27.84:8520",
"4.156.78.45:80",
"3.101.76.84:18242",
"205.198.65.77:80",
"195.158.8.123:3128",
"5.78.129.53:80",
"4.245.123.244:80",
"92.67.186.210:80",
"23.247.136.248:80",
"23.247.136.254:80",
"78.47.127.91:80",
"45.146.163.31:80",
"4.195.16.140:80",
"108.141.130.146:80",
"124.108.6.20:8085",
"59.7.246.4:80",
"95.47.239.65:3128",
"89.117.145.245:3128",
"179.60.53.25:999",
"41.59.90.171:80",
"185.123.101.160:80",
"198.49.68.80:80",
"123.141.181.24:5031",
"103.75.119.185:80",
"37.187.74.125:80",
"41.191.203.161:80"
]

chosen_proxy = random.choice(proxy_list)

# ----- 2. Selenium Setup -----
options = Options()
options.add_argument(f'--proxy-server={chosen_proxy}')
options.add_argument('--headless=new')  # Optional: for headless mode
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ----- 3. Open Target Page -----
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/blog/home")
time.sleep(2)

# ----- 4. Extract Carousel Slides -----
all_cards = []

# Locate the carousel container
carousel = driver.find_elements(By.CSS_SELECTOR, "div.swiper-wrapper")[0]

# Get all visible cards (slides)
cards = carousel.find_elements(By.CLASS_NAME, "swiper-slide")

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
        print("Error parsing card:", e)

# ----- 5. Output Results -----
print(f"\n ✓ Scraped using proxy: {chosen_proxy}")
for i, card in enumerate(all_cards, 1):
    print(f"\nCard {i}:")
    print(f"  Title   : {card['title']}")
    print(f"  Author  : {card['author']}")
    print(f"  Comments: {card['comments']}")
    print(f"  Views   : {card['views']}")

# ----- 6. Cleanup -----
driver.quit()
