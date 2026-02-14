"""Test Gemini API with curl_cffi browser impersonation (bypass geo-block)."""
import os
os.chdir('/opt/identityprism-bot')
from dotenv import load_dotenv
load_dotenv()

from curl_cffi import requests as cffi_requests
import json

API_KEY = os.getenv('GEMINI_API_KEY')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}'

payload = {
    "contents": [{"parts": [{"text": "Say hello in exactly 5 words"}]}]
}

# Test 1: curl_cffi with Chrome impersonation (no proxy)
print("Test 1: curl_cffi chrome131 impersonation (NO proxy)")
try:
    r = cffi_requests.post(URL, json=payload, impersonate="chrome131", timeout=15)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        text = r.json()['candidates'][0]['content']['parts'][0]['text']
        print(f"  Response: {text}")
    else:
        print(f"  Body: {r.text[:200]}")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 2: curl_cffi with Safari impersonation
print("\nTest 2: curl_cffi safari18_0 impersonation (NO proxy)")
try:
    r = cffi_requests.post(URL, json=payload, impersonate="safari18_0", timeout=15)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        text = r.json()['candidates'][0]['content']['parts'][0]['text']
        print(f"  Response: {text}")
    else:
        print(f"  Body: {r.text[:200]}")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 3: curl_cffi through our squid proxy
print("\nTest 3: curl_cffi chrome131 via squid proxy")
try:
    r = cffi_requests.post(URL, json=payload, impersonate="chrome131", timeout=15,
                           proxy="http://ipbot:Kx9mR4vT7nZp2W@127.0.0.1:8734")
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        text = r.json()['candidates'][0]['content']['parts'][0]['text']
        print(f"  Response: {text}")
    else:
        print(f"  Body: {r.text[:200]}")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 4: curl_cffi through residential US proxy
GEMINI_PROXY = os.getenv('GEMINI_PROXY', '')
if GEMINI_PROXY:
    print(f"\nTest 4: curl_cffi chrome131 via residential proxy")
    try:
        r = cffi_requests.post(URL, json=payload, impersonate="chrome131", timeout=15,
                               proxy=GEMINI_PROXY)
        print(f"  HTTP {r.status_code}")
        if r.status_code == 200:
            text = r.json()['candidates'][0]['content']['parts'][0]['text']
            print(f"  Response: {text}")
        else:
            print(f"  Body: {r.text[:200]}")
    except Exception as e:
        print(f"  FAIL: {e}")
