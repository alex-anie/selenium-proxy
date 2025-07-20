import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Proxy list (public proxies may be unreliable)
proxy_list = [
    "195.158.8.123:3128",
    "85.215.64.49:80",
    "161.35.70.249:8080",
    "139.59.1.14:80"
]

# Randomly choose one
proxy = random.choice(proxy_list)

# Set up Selenium with proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server=http://{proxy}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--headless=new')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    url = "https://ipinfo.io/json"
    driver.get(url)

    # Wait for page to load and extract the raw JSON text
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )
    json_text = driver.find_element(By.TAG_NAME, "pre").text
    data = json.loads(json_text)

    # Extract details
    print(Fore.GREEN + f"\n✅ Proxy Used     : {proxy}")
    print(Fore.CYAN + f"🌐 IP Address     : {data.get('ip', 'N/A')}")
    print(Fore.CYAN + f"🏙️  City           : {data.get('city', 'N/A')}")
    print(Fore.CYAN + f"📍 Region         : {data.get('region', 'N/A')}")
    print(Fore.CYAN + f"🌍 Country        : {data.get('country', 'N/A')}")
    print(Fore.CYAN + f"⏰ Timezone       : {data.get('timezone', 'N/A')}")
    print(Fore.CYAN + f"🔌 ISP (Org)      : {data.get('org', 'N/A')}")
    print(Fore.CYAN + f"📡 Location (Lat,Lon): {data.get('loc', 'N/A')}")

except Exception as e:
    print(Fore.RED + f"\n❌ Error: {e}")
finally:
    driver.quit()
