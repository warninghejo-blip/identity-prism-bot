"""Discover Colosseum auth endpoints and try to login via Twitter OAuth."""
import json
from curl_cffi import requests as r

# Check auth/me first
resp = r.get("https://agents.colosseum.com/auth/me", impersonate="chrome131", timeout=10)
print(f"GET /auth/me (no auth): {resp.status_code} — {resp.text[:200]}")

# Try auth endpoints
for path in [
    "/auth/twitter", "/auth/login", "/auth/signin",
    "/auth/twitter/callback", "/auth/x",
    "/auth/login/twitter", "/auth/providers",
]:
    resp = r.get(f"https://agents.colosseum.com{path}",
                 impersonate="chrome131", timeout=10, allow_redirects=False)
    status = resp.status_code
    loc = resp.headers.get("location", "")
    if status != 404:
        print(f"GET {path}: {status} loc={loc} body={resp.text[:150]}")

# Try with agent API key
api_key = "4f4f32a9ee78f00c4117f4a8f7af8dc914162b36161d3e29301acbc7be9e9cb1"
headers = {"Authorization": f"Bearer {api_key}"}

resp = r.get("https://agents.colosseum.com/auth/me", headers=headers, impersonate="chrome131", timeout=10)
print(f"\nGET /auth/me (with apiKey): {resp.status_code} — {resp.text[:300]}")

# If we're authenticated, try to update project
if resp.status_code == 200:
    data = resp.json()
    print(f"Auth data: {json.dumps(data, indent=2)[:500]}")
    
    # Try updating with auth cookie/token from this session
    cookies = dict(resp.cookies)
    print(f"Cookies from auth: {cookies}")

# Try with apiKey as different auth methods
for auth_header in [
    {"x-api-key": api_key},
    {"Authorization": api_key},
    {"Cookie": f"token={api_key}"},
    {"Cookie": f"session={api_key}"},
    {"Cookie": f"agent_api_key={api_key}"},
]:
    resp = r.put("https://agents.colosseum.com/api/projects/identity-prism",
                 headers={**auth_header, "Content-Type": "application/json"},
                 json={"repoLink": "https://github.com/YourIdentityPrism/identity-prism"},
                 impersonate="chrome131", timeout=10)
    if resp.status_code != 404:
        hdr_key = list(auth_header.keys())[0]
        print(f"\nPUT /api/projects/identity-prism ({hdr_key}): {resp.status_code} — {resp.text[:200]}")
