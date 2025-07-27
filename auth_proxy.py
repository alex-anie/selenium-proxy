import zipfile
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------
# Proxy credentials & info
# -------------------------
proxy_host = "proxy.example.com"   # Replace with actual proxy host
proxy_port = "8080"                # Replace with actual proxy port
proxy_user = "your_username"       # Replace with your proxy username
proxy_pass = "your_password"       # Replace with your proxy password

# Target URL to visit after setting up the proxy
test_url = "https://ipinfo.io/json"  # You can replace with any website you want

# -------------------------
# Create Chrome extension to handle proxy auth
# -------------------------

plugin_file = 'proxy_auth_plugin.zip'

manifest_json = f"""
{{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Proxy Auth Extension",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {{
        "scripts": ["background.js"]
    }},
    "minimum_chrome_version":"22.0.0"
}}
"""

background_js = f"""
var config = {{
        mode: "fixed_servers",
        rules: {{
        singleProxy: {{
            scheme: "http",
            host: "{proxy_host}",
            port: parseInt({proxy_port})
        }},
        bypassList: ["localhost"]
        }}
    }};

chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{proxy_user}",
            password: "{proxy_pass}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {{urls: ["<all_urls>"]}},
    ['blocking']
);
"""

# Create ZIP file with the extension content
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

# -------------------------
# Set up Chrome options
# -------------------------
options = Options()
options.add_argument('--headless=new')
options.add_extension(plugin_file)

# Optional: Remove "automated" detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# -------------------------
# Start Chrome WebDriver
# -------------------------
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# -------------------------
# Visit the target URL
# -------------------------
try:
    print("🔄 Opening target page using authenticated proxy...\n")
    driver.get(test_url)
    time.sleep(3)

    # Retrieve and display IP address from response
    body = driver.find_element(By.TAG_NAME, "body").text
    print("✅ Proxy Auth Worked — Page Output:\n")
    print(body)

except Exception as e:
    print("❌ Failed to load page or extract content:", e)

finally:
    driver.quit()

# -------------------------
# Cleanup plugin file
# -------------------------
if os.path.exists(plugin_file):
    os.remove(plugin_file)
