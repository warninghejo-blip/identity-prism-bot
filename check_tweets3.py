import os
from dotenv import load_dotenv
load_dotenv()
from curl_cffi import requests as r

api_key = os.getenv("TWITTERAPI_IO_API_KEY")
headers = {"X-API-Key": api_key}
resp = r.get(
    "https://api.twitterapi.io/twitter/tweet/advanced_search",
    params={"query": "from:Identity_Prism", "queryType": "Latest"},
    headers=headers,
    impersonate="chrome131",
    timeout=30,
)
d = resp.json()
tweets = d.get("tweets") or []
print(f"Found {len(tweets)} tweets")
for t in tweets[:5]:
    print(f"[{t.get('createdAt','')}] {t.get('text','?')[:200]}")
    print("-" * 60)
