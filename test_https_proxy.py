import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init
from config_proxy import find_https_proxy

init(autoreset=True)

# Get a working HTTPS proxy
working_proxy = find_https_proxy()
if not working_proxy:
    print(Fore.RED + "❌ No HTTPS proxy found. Exiting script.")
    exit()

# Configure Chrome with the working HTTPS proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server=http://{working_proxy}')
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--ignore-certificate-errors')  # Helps avoid SSL warnings

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# Visit HTTPS test site
try:
    driver.get("https://ipinfo.io/json")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )
    json_text = driver.find_element(By.TAG_NAME, "pre").text
    data = json.loads(json_text)

    print(Fore.GREEN + f"\n🛡️ Successfully connected using proxy: {working_proxy}")
    print(Fore.CYAN + f"🌐 IP Address : {data.get('ip', 'N/A')}")
    print(Fore.CYAN + f"🌍 Country    : {data.get('country', 'N/A')}")
    print(Fore.CYAN + f"🔌 ISP (Org)  : {data.get('org', 'N/A')}")
    print(Fore.CYAN + f"📍 Location   : {data.get('loc', 'N/A')}")
except Exception as e:
    print(Fore.RED + f"\n❌ Failed to load page with proxy {working_proxy} — {e}")
finally:
    driver.quit()
