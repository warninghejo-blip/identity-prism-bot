"""Submit the project for judging."""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets = json.loads(Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json").read_text())
api_key = secrets["apiKey"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

resp = r.post("https://agents.colosseum.com/api/my-project/submit",
              headers=headers, impersonate="chrome131", timeout=30)
print(f"POST /api/my-project/submit: {resp.status_code}")
print(f"Response: {resp.text[:500]}")
