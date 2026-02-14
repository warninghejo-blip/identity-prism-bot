import os
os.chdir('/opt/identityprism-bot')
from dotenv import load_dotenv
load_dotenv()
k = os.getenv('GEMINI_API_KEY', '')
print(f'Key len={len(k)} starts={k[:8]} ends={k[-4:]}')

from curl_cffi import requests as cr
import json

# Test with key in header instead of URL param
url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
payload = {"contents": [{"parts": [{"text": "Say hi in 5 words"}]}]}

print('\nTest A: curl_cffi chrome131, key in URL param')
try:
    r = cr.post(f'{url}?key={k}', json=payload, impersonate='chrome131', timeout=15)
    print(f'  HTTP {r.status_code} -> {r.text[:200]}')
except Exception as e:
    print(f'  FAIL: {e}')

print('\nTest B: curl_cffi chrome131, key in x-goog-api-key header')
try:
    r = cr.post(url, json=payload, impersonate='chrome131', timeout=15,
                headers={'x-goog-api-key': k, 'Content-Type': 'application/json'})
    print(f'  HTTP {r.status_code} -> {r.text[:200]}')
except Exception as e:
    print(f'  FAIL: {e}')

print('\nTest C: curl_cffi chrome131, key in header, via residential proxy')
proxy = os.getenv('GEMINI_PROXY', '')
if proxy:
    try:
        r = cr.post(url, json=payload, impersonate='chrome131', timeout=15,
                    headers={'x-goog-api-key': k, 'Content-Type': 'application/json'},
                    proxy=proxy)
        print(f'  HTTP {r.status_code} -> {r.text[:200]}')
    except Exception as e:
        print(f'  FAIL: {e}')
