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
print(f"Status: {resp.status_code}")
print(f"Body: {resp.text[:1000]}")
