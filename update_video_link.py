"""Update Colosseum project presentationLink with YouTube video via PUT /my-project."""
import json
from curl_cffi import requests as r

secrets = json.load(open('/opt/identityprism-bot/secrets/colosseum-hackathon.json'))
h = {'Authorization': 'Bearer ' + secrets['apiKey'], 'Content-Type': 'application/json'}
BASE = 'https://agents.colosseum.com/api'

# Step 1: Get current project
print("Getting current project...")
resp = r.get(f'{BASE}/my-project', headers=h, impersonate='chrome131', timeout=15)
print(f"  GET /my-project: {resp.status_code}")
if resp.status_code == 200:
    proj = resp.json().get('project', {})
    print(f"  presentationLink: {proj.get('presentationLink', '(not set)')}")

# Step 2: Update with presentationLink
print("\nUpdating presentationLink...")
data = {'presentationLink': 'https://www.youtube.com/shorts/z_FC8T5Q7Ec'}
resp = r.put(f'{BASE}/my-project', headers=h, json=data, impersonate='chrome131', timeout=15)
print(f"  PUT /my-project: {resp.status_code}")
print(f"  Response: {resp.text[:500]}")

# Step 3: Verify
print("\nVerifying...")
resp = r.get(f'{BASE}/my-project', headers=h, impersonate='chrome131', timeout=15)
if resp.status_code == 200:
    proj = resp.json().get('project', {})
    print(f"  presentationLink: {proj.get('presentationLink', '(not set)')}")
    print(f"  liveAppLink: {proj.get('liveAppLink', '(not set)')}")
    print(f"  status: {proj.get('status', '?')}")
else:
    print(f"  Verify failed: {resp.status_code}")
