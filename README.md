# 🕵️‍♂️ How to Use a Proxy With Selenium (with LambdaTest Integration)

This project demonstrates how to perform **web scraping and testing using Selenium with rotating proxies** in Python. It includes multiple practical scripts, including one configured to run on [LambdaTest](https://www.lambdatest.com/) for cross-browser cloud testing.

---

## 📦 Requirements

Make sure to install the following Python packages:

```bash
pip install selenium webdriver-manager python-dotenv
```

> ✅ Optionally, you can also install `colorama` to enable colored terminal output (used in some scripts):
```bash
pip install colorama
```

---

## 📁 Project Files

### ✔️ Main Scripts

| File | Purpose |
|------|---------|
| `track.py` | Cloud-enabled script configured with **LambdaTest**. Scrapes a product page via a proxy. |
| `scrape_blog.py` | Scrapes a blog article page using a working proxy. Can be run locally. |
| `track_product.py` | Scrapes product info from LambdaTest's demo e-commerce store using a proxy. |
| `proxy_geo_checker.py` | Detects your IP, country, city, timezone, and ISP using a proxy (great for IP rotation tests). |
| `proxy_utils.py` | Utility file that fetches and validates working HTTP proxies. **Not meant to be run directly.** It is imported and reused in all other scripts. |

---

## 🧪 Running the Scripts

### 1. ✅ Setup
Before running, ensure you have Python 3.9+ installed and a working internet connection.

#### a. Clone the repo and create a virtual environment:
```bash
git clone https://github.com/alex-anie/selenium-proxy
cd selenium-proxy
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

#### b. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🌐 Running Locally

Each script uses the shared proxy helper module `proxy_utils.py`.

### ➤ To scrape a blog:
```bash
python scrape_blog.py
```

### ➤ To track a product on LambdaTest’s e-commerce demo store:
```bash
python track_product.py
```

### ➤ To test your proxy's location/IP/ISP info:
```bash
python proxy_geo_checker.py
```

---

## ☁️ Running on LambdaTest

> `track.py` is configured to run the test in **LambdaTest cloud environment**.

### ✅ To run it:
1. Update your **LambdaTest username and access key** in the `.env` file or directly in `track.py`.
2. Then run:
```bash
python track.py
```

> This will launch the test in a remote browser session with proxy enabled, powered by LambdaTest.

---

## 🧠 About the Project

This project was built as a comprehensive demo of:

- Using **rotating HTTP proxies** with Selenium
- Automating **web scraping tasks**
- Handling proxy errors, timeouts, and fallbacks
- **Cloud testing** with LambdaTest for cross-platform/browser reliability
- Modular and reusable Python code structure

Each script uses a shared proxy-checking utility that verifies which proxies are functional before running the main test. This allows users to easily plug in any of these examples for automation, scraping, or learning purposes.

---
