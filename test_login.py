import os
from dotenv import load_dotenv
load_dotenv()

from curl_cffi import requests as r

proxy = os.getenv('TWITTERAPI_IO_PROXIES', '').split(',')[0].strip()
api_key = os.getenv('TWITTERAPI_IO_API_KEY', '')

print(f"Proxy: {proxy}")
print(f"API Key: {api_key[:10]}...")

payload = {
    'user_name': os.getenv('TWITTERAPI_IO_USERNAME'),
    'email': os.getenv('TWITTERAPI_IO_EMAIL'),
    'password': os.getenv('TWITTERAPI_IO_PASSWORD'),
    'proxy': proxy,
    'totp_secret': os.getenv('TWITTERAPI_IO_TOTP_SECRET'),
}
print(f"Username: {payload['user_name']}")
print(f"Email: {payload['email']}")

headers = {'X-API-Key': api_key}

print("\n=== Login attempt ===")
try:
    resp = r.post(
        'https://api.twitterapi.io/twitter/user_login_v2',
        json=payload,
        headers=headers,
        impersonate='chrome131',
        timeout=60,
    )
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
