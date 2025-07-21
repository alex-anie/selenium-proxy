import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from proxy_utils import find_working_proxy

def setup_browser_with_proxy(proxy: str, timeout=10):
    options = Options()
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--start-maximized")
    options.page_load_strategy = 'normal'
    return webdriver.Chrome(options=options)

def extract_jobs(driver):
    jobs = []
    try:
        job_cards = driver.find_elements(By.CSS_SELECTOR, "tr.job")
        for job in job_cards:
            try:
                title = job.find_element(By.CSS_SELECTOR, "td.position h2").text
                jobs.append(title)
            except:
                continue
    except Exception as e:
        print("⚠️ Failed to extract job listings:", e)
    return jobs

def main():
    TEST_URL = "https://httpbin.org/ip"
    TARGET_URL = "https://remoteok.io/"

    print("🔍 Finding working proxy...")
    proxy = find_working_proxy(TEST_URL)
    if not proxy:
        print("❌ No working proxy found.")
        return

    try:
        driver = setup_browser_with_proxy(proxy)
        driver.set_page_load_timeout(15)
        driver.get(TARGET_URL)
        time.sleep(5)

        print("✅ Page loaded. Scraping jobs...")
        job_titles = extract_jobs(driver)
        print(f"🧠 Found {len(job_titles)} jobs:\n")
        for job in job_titles:
            print(f"• {job}")

    except TimeoutException:
        print("⏱️ Page load timed out.")
    except WebDriverException as e:
        print(f"🚨 WebDriver error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
