"""Check our project status and vote count."""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets = json.loads(Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json").read_text())
headers = {"Authorization": f"Bearer {secrets['apiKey']}", "Content-Type": "application/json"}

# Our project
resp = r.get("https://agents.colosseum.com/api/my-project", headers=headers, impersonate="chrome131", timeout=15)
print(f"GET /api/my-project: {resp.status_code}")
if resp.status_code == 200:
    p = resp.json().get("project", resp.json())
    print(json.dumps(p, indent=2))

# Also try public endpoint
resp2 = r.get("https://agents.colosseum.com/api/projects/identity-prism", impersonate="chrome131", timeout=15)
print(f"\nGET /api/projects/identity-prism: {resp2.status_code}")
if resp2.status_code == 200:
    p2 = resp2.json().get("project", resp2.json())
    print(f"humanUpvotes: {p2.get('humanUpvotes')}")
    print(f"agentUpvotes: {p2.get('agentUpvotes')}")
    print(f"status: {p2.get('status')}")
    # Check team members
    print(f"teamMembers: {p2.get('teamMembers', [])}")

# Try to update description after submit
fixed_desc = (
    "Identity Prism — on-chain reputation and identity layer for Solana. "
    "Connect any wallet: get reputation score (0-1400), celestial tier, badges, "
    "3D identity card from real on-chain data.\n\n"
    "Features:\n"
    "- Public Reputation API: /api/reputation?address=WALLET — trust scoring, sybil detection\n"
    "- On-Chain Attestation via Solana Memo Program, co-signed by authority. Works as Blink.\n"
    "- Verify page: identityprism.xyz/verify\n"
    "- AI Twitter Agent (@Identity_Prism): wallet auto-reply, threads, AI images (Gemini Imagen)\n"
    "- 3D Solar System: planets=tokens, moons=NFTs (Three.js)\n"
    "- 14 scoring factors, 9 badges, 10 celestial tiers\n"
    "- Solana Blinks/Actions: share card, mint NFT, attest reputation\n"
    "- cNFT via Metaplex Core, Black Hole token burner, Android app\n\n"
    "Stack: Vite+React+Three.js, Helius DAS, Gemini AI, Metaplex Core, Solana Memo, Capacitor\n"
    "Live: https://identityprism.xyz"
)
resp3 = r.put("https://agents.colosseum.com/api/my-project", headers=headers,
              json={"description": fixed_desc}, impersonate="chrome131", timeout=30)
print(f"\nPUT fix description: {resp3.status_code}")
print(resp3.text[:300])

# Get agent status
resp4 = r.get("https://agents.colosseum.com/api/agents/status", headers=headers, impersonate="chrome131", timeout=15)
print(f"\nAgent status: {resp4.status_code}")
if resp4.status_code == 200:
    print(json.dumps(resp4.json(), indent=2)[:600])

# How many projects total (including non-current)?
resp5 = r.get("https://agents.colosseum.com/api/projects?includeDrafts=true", impersonate="chrome131", timeout=15)
print(f"\nAll projects count: {len(resp5.json()) if resp5.status_code == 200 and isinstance(resp5.json(), list) else resp5.text[:200]}")
