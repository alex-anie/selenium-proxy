import time
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from proxy_utils import find_working_proxy  # ✅ Uses your existing utility
from colorama import Fore, init

init(autoreset=True)

# List of target HTTPS test URLs
test_urls = [
    "https://ipinfo.io/json",
    "https://api.myip.com",  # Optional second test service
]

# Number of proxy sessions to run
proxy_sessions = 3

def configure_browser(proxy):
    """Configure Chrome WebDriver with proxy and security options"""
    options = Options()
    options.add_argument(f'--proxy-server=https://{proxy}')  # HTTPS proxy
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')  # Useful for proxy SSL
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for session in range(proxy_sessions):
    print(Fore.YELLOW + f"\n🧪 Running proxy session {session + 1} of {proxy_sessions}")

    # Choose a test endpoint
    target_url = random.choice(test_urls)

    # Get a working HTTPS proxy from the pool
    proxy = find_working_proxy(target_url)
    if not proxy:
        print(Fore.RED + "❌ No working proxy found for this session.\n")
        continue

    # Launch Chrome with proxy
    driver = configure_browser(proxy)

    try:
        driver.get(target_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        raw_json = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(raw_json)

        print(Fore.GREEN + f"✅ Proxy Used: {proxy}")
        print(Fore.CYAN + f"🌐 IP Address: {data.get('ip', 'N/A')}")
        print(Fore.CYAN + f"🌍 Country    : {data.get('country', 'N/A')}")
        print(Fore.CYAN + f"🔌 ISP (Org)  : {data.get('org', 'N/A')}")
        print(Fore.CYAN + f"📡 Location   : {data.get('loc', 'N/A')}")

    except Exception as e:
        print(Fore.RED + f"❌ Proxy failed during test: {proxy} — {e}")
    finally:
        driver.quit()
        time.sleep(2)  # Avoid rapid hammering of proxies
