from curl_cffi import requests as r
import json, os
from dotenv import load_dotenv
load_dotenv()

proxy = "http://ipbot:Kx9mR4vT7nZp2W@188.137.250.160:8734"
px = {"https": proxy, "http": proxy}

print("=== Test 1: Proxy connectivity ===")
try:
    resp = r.get("https://httpbin.org/ip", impersonate="chrome131", proxies=px, timeout=15)
    print(f"OK - IP: {resp.json()}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n=== Test 2: twitterapi.io login ===")
api_key = os.getenv("TWITTERAPI_IO_API_KEY", "")
username = os.getenv("TWITTERAPI_IO_USERNAME", "")
email = os.getenv("TWITTERAPI_IO_EMAIL", "")
password = os.getenv("TWITTERAPI_IO_PASSWORD", "")
totp = os.getenv("TWITTERAPI_IO_TOTP_SECRET", "")

headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
login_payload = {
    "username": username,
    "email": email, 
    "password": password,
    "totp_secret": totp,
}
try:
    resp = r.post(
        "https://api.twitterapi.io/twitter/auth/login",
        json=login_payload, headers=headers,
        impersonate="chrome131", proxies=px, timeout=30,
    )
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text[:500]}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n=== Test 3: twitterapi.io search (no login needed) ===")
try:
    resp = r.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        params={"query": "solana", "queryType": "Top", "cursor": ""},
        headers={"X-API-Key": api_key},
        impersonate="chrome131", proxies=px, timeout=30,
    )
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text[:300]}")
except Exception as e:
    print(f"FAIL: {e}")
