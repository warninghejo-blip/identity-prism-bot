"""Check Colosseum secrets file structure and try API."""
import json
from pathlib import Path

secrets_path = Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json")
with open(secrets_path) as f:
    secrets = json.load(f)
print("Keys in secrets:", list(secrets.keys()))
for k, v in secrets.items():
    if isinstance(v, str) and len(v) > 10:
        print(f"  {k}: {v[:8]}...{v[-4:]} ({len(v)} chars)")
    else:
        print(f"  {k}: {v}")

from curl_cffi import requests as r

# Try /agents/me endpoint
api_key = secrets.get("api_key") or secrets.get("apiKey") or secrets.get("token") or secrets.get("auth_token") or ""
if not api_key:
    print("\nNo API key found in secrets. Trying other fields...")
    for k, v in secrets.items():
        if isinstance(v, str) and len(v) > 20:
            api_key = v
            print(f"  Trying field '{k}' as API key")
            break

if api_key:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = r.get("https://agents.colosseum.com/api/agents/me", headers=headers, impersonate="chrome131", timeout=15)
    print(f"\n/agents/me: {resp.status_code}")
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False)[:2000])
    else:
        print(resp.text[:500])
