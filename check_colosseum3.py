"""Check Colosseum project submission details."""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets_path = Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json")
with open(secrets_path) as f:
    secrets = json.load(f)

api_key = secrets["apiKey"]
agent_id = secrets["agent_id"]
project_id = secrets["project_id"]
project_slug = secrets["project_slug"]
team_id = secrets["team_id"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Try various endpoints
endpoints = [
    f"/agents/{agent_id}",
    f"/agents/{agent_id}/status",
    f"/projects/{project_id}",
    f"/projects/{project_slug}",
    f"/teams/{team_id}",
    f"/teams/{team_id}/project",
]

for ep in endpoints:
    resp = r.get(f"https://agents.colosseum.com/api{ep}", headers=headers, impersonate="chrome131", timeout=15)
    status = resp.status_code
    body = resp.text[:300] if status != 404 else "404"
    print(f"GET {ep}: {status}")
    if status == 200:
        try:
            data = resp.json()
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])
        except:
            print(body)
    print()
