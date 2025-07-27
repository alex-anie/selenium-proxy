import requests

from colorama import init, Fore, Style
init(autoreset=True)


# List of proxies to check from https://free-proxy-list.net/en/#
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

def find_working_proxy(test_url, proxies=proxy_list, timeout=5):
    """Return first working proxy that gives 200 status for test_url."""
    for proxy in proxies:
        proxy_conf = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        try:
            print(Fore.YELLOW + f"Please wait! program is currently routing for the correct `proxy`")

            response = requests.get(test_url, proxies=proxy_conf, timeout=timeout)
            if response.status_code == 200:
                print(Fore.GREEN + f"✓ Working proxy found: {proxy}\033[0m")
                return proxy
            else:
                print(Fore.RED + f"× Bad status from {proxy}: {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"× Proxy failed: {proxy} — {e}")
    return None
