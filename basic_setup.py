# -- some imported code above
from selenium import webdriver

# --- Usage Example ---
proxy = "195.158.8.123:3128"
username = "yourUsername"     # Set to None if not needed
password = "yourPassword"     # Set to None if not needed

try:
    driver = get_driver_with_proxy(proxy, username, password)
    driver.get("https://httpbin.org/ip")
    time.sleep(2)
    print(driver.page_source)
except TimeoutException:
    print("❌ Proxy timed out.")
except WebDriverException as e:
    print(f"❌ WebDriver Error: {e}")
finally:
    try:
        driver.quit()
    except:
        pass
