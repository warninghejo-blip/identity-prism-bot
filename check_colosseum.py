"""Check Colosseum project submission details."""
import json, os
from pathlib import Path

secrets_path = Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json")
with open(secrets_path) as f:
    secrets = json.load(f)

agent_id = secrets.get("agent_id")
project_id = secrets.get("project_id")
api_key = secrets.get("api_key", "")
print(f"Agent ID: {agent_id}")
print(f"Project ID: {project_id}")
print(f"API Key: {'SET' if api_key else 'MISSING'} ({len(api_key)} chars)")

# Fetch project details
from curl_cffi import requests as r
headers = {"Authorization": f"Bearer {api_key}"}
resp = r.get(f"https://agents.colosseum.com/api/agents/{agent_id}", headers=headers, impersonate="chrome131", timeout=15)
print(f"\nAgent endpoint: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])

resp2 = r.get(f"https://agents.colosseum.com/api/projects/{project_id}", headers=headers, impersonate="chrome131", timeout=15)
print(f"\nProject endpoint: {resp2.status_code}")
if resp2.status_code == 200:
    data2 = resp2.json()
    print(json.dumps(data2, indent=2, ensure_ascii=False)[:3000])
