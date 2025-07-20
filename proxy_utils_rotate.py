import random
import requests

proxy_list = [
    "http://85.215.64.49:80",
    "http://161.35.70.249:8080",
    "http://139.59.1.14:80",
    "http://195.158.8.123:3128",
    "http://5.78.129.53:80",
]

def find_working_proxy(test_url: str, timeout: int = 5):
    print("🔍 Checking available proxies...")

    for proxy in proxy_list:
        try:
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                print(f"✅ Working proxy found: {proxy}")
                return proxy
            else:
                print(f"⚠️ Proxy {proxy} failed with status {response.status_code}")
        except Exception as e:
            print(f"❌ Proxy {proxy} failed: {e}")

    return None
