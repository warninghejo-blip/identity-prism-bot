import os
from dotenv import load_dotenv
load_dotenv()
from curl_cffi import requests as r

api_key = os.getenv("TWITTERAPI_IO_API_KEY")
headers = {"X-API-Key": api_key}
resp = r.get(
    "https://api.twitterapi.io/twitter/user_tweets",
    params={"userName": "Identity_Prism"},
    headers=headers,
    impersonate="chrome131",
    timeout=30,
)
data = resp.json()
for t in (data.get("tweets") or [])[:5]:
    print(f"[{t.get('createdAt','')}] {t.get('text','?')[:200]}")
    print("-" * 60)
