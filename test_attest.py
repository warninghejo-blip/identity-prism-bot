"""Test the attestation endpoint POST."""
from curl_cffi import requests as r
import json

resp = r.post(
    "http://localhost:8787/api/actions/attest?address=vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg",
    json={"account": "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"},
    impersonate="chrome131",
    timeout=30,
)
data = resp.json()
if "transaction" in data:
    print(f"SUCCESS! Transaction length: {len(data['transaction'])} chars")
    print(f"Message: {data.get('message', '')}")
else:
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
