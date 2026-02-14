"""Complete the Colosseum Twitter OAuth flow programmatically."""
import json
from pathlib import Path
from curl_cffi import requests as r

# Load Twitter cookies
cookies_path = Path("/opt/identityprism-bot/cookies.json")
twitter_cookies = json.loads(cookies_path.read_text())
cookie_dict = {c["name"]: c["value"] for c in twitter_cookies}
print(f"Twitter cookies: {list(cookie_dict.keys())}")

# Step 1: Find OAuth initiation URL from Colosseum
# Try GET /auth/twitter which should redirect to Twitter OAuth
session = r.Session(impersonate="chrome131")

# First check what endpoints exist
for path in ["/auth/twitter", "/auth/twitter/login", "/auth/login/twitter", "/auth/x/login"]:
    resp = session.get(f"https://agents.colosseum.com{path}", 
                       allow_redirects=False, timeout=10)
    if resp.status_code != 404:
        loc = resp.headers.get("location", "")
        print(f"GET {path}: {resp.status_code} loc={loc[:200]}")
        if resp.status_code in (301, 302, 307) and ("twitter" in loc or "x.com" in loc):
            print(f"  >>> FOUND OAuth redirect!")

# Step 2: Try the Colosseum web app auth flow
# The SvelteKit app likely POSTs to a form action
for path in ["/auth/twitter", "/auth/login", "/auth/signin"]:
    resp = session.post(f"https://agents.colosseum.com{path}",
                        allow_redirects=False, timeout=10)
    if resp.status_code != 404:
        loc = resp.headers.get("location", "")
        print(f"POST {path}: {resp.status_code} loc={loc[:200]}")

# Step 3: Try the main colosseum.com auth endpoints
for path in ["/auth/twitter", "/auth/login", "/api/auth/twitter", "/api/auth/signin/twitter"]:
    resp = session.get(f"https://colosseum.com{path}",
                       allow_redirects=False, timeout=10)
    if resp.status_code != 404:
        loc = resp.headers.get("location", "")
        print(f"GET colosseum.com{path}: {resp.status_code} loc={loc[:200]}")

# Step 4: Try to follow the full OAuth flow if we found a redirect
# First, let's see what the Colosseum SvelteKit app does when "Sign in with X" is clicked
# It likely fetches from the agents API
resp = session.get("https://agents.colosseum.com/auth/twitter",
                   allow_redirects=True, timeout=15)
print(f"\nFull redirect chain for /auth/twitter:")
print(f"  Final URL: {resp.url}")
print(f"  Status: {resp.status_code}")
print(f"  Body: {resp.text[:300]}")

# Try with POST
resp = session.post("https://agents.colosseum.com/auth/twitter",
                    allow_redirects=True, timeout=15)
print(f"\nPOST /auth/twitter:")
print(f"  Final URL: {resp.url}")
print(f"  Status: {resp.status_code}")
print(f"  Body: {resp.text[:300]}")

# Check session cookies after auth attempt
print(f"\nSession cookies: {dict(session.cookies)}")
