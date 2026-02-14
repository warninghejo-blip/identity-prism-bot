import os
from dotenv import load_dotenv
load_dotenv('/opt/identityprism-bot/.env', override=True)
k = os.getenv('GEMINI_API_KEY', '')
proxy = os.getenv('GEMINI_PROXY', '')
print(f'Key len={len(k)} starts={k[:8]}')
print(f'Proxy={proxy[:30]}')

from curl_cffi import requests as cr

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
payload = {"contents": [{"parts": [{"text": "Say hi in 5 words"}]}]}

print('\nTest 1: chrome131 direct (no proxy)')
try:
    r = cr.post(f'{url}?key={k}', json=payload, impersonate='chrome131', timeout=15)
    print(f'  HTTP {r.status_code}')
    if r.status_code == 200:
        print(f'  OK: {r.json()["candidates"][0]["content"]["parts"][0]["text"]}')
    else:
        print(f'  {r.text[:200]}')
except Exception as e:
    print(f'  FAIL: {e}')

print('\nTest 2: chrome131 via residential proxy')
try:
    r = cr.post(f'{url}?key={k}', json=payload, impersonate='chrome131', timeout=15, proxy=proxy)
    print(f'  HTTP {r.status_code}')
    if r.status_code == 200:
        print(f'  OK: {r.json()["candidates"][0]["content"]["parts"][0]["text"]}')
    else:
        print(f'  {r.text[:200]}')
except Exception as e:
    print(f'  FAIL: {e}')

print('\nTest 3: chrome131 via squid proxy (server)')
try:
    r = cr.post(f'{url}?key={k}', json=payload, impersonate='chrome131', timeout=15,
                proxy='http://ipbot:Kx9mR4vT7nZp2W@127.0.0.1:8734')
    print(f'  HTTP {r.status_code}')
    if r.status_code == 200:
        print(f'  OK: {r.json()["candidates"][0]["content"]["parts"][0]["text"]}')
    else:
        print(f'  {r.text[:200]}')
except Exception as e:
    print(f'  FAIL: {e}')
