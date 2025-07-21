import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from proxy_utils import find_working_proxy
from colorama import Fore, init

init(autoreset=True)

def setup_driver_with_proxy(proxy: str) -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless=new")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def scrape_google_results(query: str, retries: int = 3):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    for attempt in range(1, retries + 1):
        print(Fore.CYAN + f"\n🔁 Attempt {attempt} of {retries}")
        proxy = find_working_proxy(test_url="https://www.google.com")
        if not proxy:
            print(Fore.RED + "❌ No working proxy found.")
            return

        driver = setup_driver_with_proxy(proxy)
        driver.set_page_load_timeout(15)

        try:
            driver.get(search_url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )

            # CAPTCHA or block detection
            if "sorry" in driver.current_url or "interstitial" in driver.current_url:
                raise Exception("Blocked or CAPTCHA detected")

            results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
            print(Fore.GREEN + f"\n🔍 Top Google Results for: '{query}' using proxy {proxy}")
            for i, result in enumerate(results[:5], start=1):
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    print(f"{i}. {title} - {link}")
                except:
                    continue

            driver.quit()
            break  # Success

        except Exception as e:
            print(Fore.RED + f"⚠️ Failed attempt {attempt}: {e}")
            driver.quit()
            time.sleep(2)

    else:
        print(Fore.RED + "\n❌ All attempts failed. Try again later.")

# Run script
if __name__ == "__main__":
    scrape_google_results("open source ecommerce platforms")
