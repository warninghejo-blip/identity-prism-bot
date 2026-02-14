"""Update project via correct endpoint: PUT /api/my-project"""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets = json.loads(Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json").read_text())
api_key = secrets["apiKey"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Step 1: Check current project
resp = r.get("https://agents.colosseum.com/api/my-project", headers=headers, impersonate="chrome131", timeout=15)
print(f"GET /api/my-project: {resp.status_code}")
if resp.status_code == 200:
    proj = resp.json()
    print(json.dumps(proj, indent=2)[:600])
    print("...")

# Step 2: Update project
update_payload = {
    "description": (
        "Identity Prism is an on-chain reputation and identity layer for Solana. "
        "Connect any wallet to get a reputation score (0-1400), celestial tier, achievement badges, "
        "and a stunning 3D identity card — all computed from real on-chain data.\n\n"
        "Core Features:\n"
        "- Reputation API (public REST): /api/reputation?address=WALLET — any dApp can integrate for trust scoring, sybil detection, or feature gating\n"
        "- On-Chain Attestation: Record reputation permanently on Solana via Memo program, co-signed by authority. Works as a Solana Blink.\n"
        "- Attestation Verify Page: identityprism.xyz/verify — verify any attestation transaction on-chain\n"
        "- AI Twitter Agent (@Identity_Prism): Auto-replies with real reputation data when mentioned with a wallet address. "
        "Posts threads, trend reactions, quotes with AI-generated images (Gemini Imagen).\n"
        "- 3D Solar System Visualization: planets=tokens, moons=NFTs, dust=activity (Three.js)\n"
        "- Multi-Factor Scoring: 14 factors including SOL balance, wallet age, tx count, NFTs, DeFi/LST positions. 13 badge types, 10 celestial tiers.\n"
        "- Solana Blinks/Actions: share identity card, mint as NFT, attest reputation — all from any Blink-compatible wallet\n"
        "- cNFT Minting via Metaplex Core\n"
        "- Black Hole: Burn unwanted SPL tokens, reclaim rent SOL\n"
        "- Android app via Capacitor + Solana Mobile Wallet Adapter\n\n"
        "Stack: Vite+React+Three.js, Node.js, Helius DAS API, Gemini AI (text+Imagen), Metaplex Core, "
        "Solana Actions/Blinks, Solana Memo Program, curl_cffi, Capacitor.\n"
        "Live: https://identityprism.xyz"
    ),
    "repoLink": "https://github.com/YourIdentityPrism/identity-prism",
    "solanaIntegration": (
        "1. Helius RPC + DAS API: Wallet tx history, token holdings, NFT collections — fed into 14-factor reputation scoring engine\n"
        "2. Solana Memo Program: On-chain attestation — writes reputation score as JSON memo, co-signed by treasury authority keypair. Verifiable by any smart contract or dApp.\n"
        "3. Metaplex Core: Mints identity cards as on-chain NFTs with full collection verification\n"
        "4. SPL Token: SOL payments for minting, token balance analysis for scoring\n"
        "5. Solana Actions/Blinks: Three Blink endpoints — share card, mint NFT, attest reputation. Works from Phantom, Backpack, Dialect.\n"
        "6. Black Hole: Burns SPL tokens (TOKEN_PROGRAM + TOKEN_2022), reclaims rent via closeAccount\n"
        "7. Reputation API: Public REST endpoints — any Solana dApp can call to assess wallet trust, gate features, or detect sybils"
    ),
    "technicalDemoLink": "https://identityprism.xyz",
    "tags": ["ai", "identity", "consumer", "infra"],
}

print("\n--- Updating project ---")
resp = r.put("https://agents.colosseum.com/api/my-project", headers=headers,
             json=update_payload, impersonate="chrome131", timeout=30)
print(f"PUT /api/my-project: {resp.status_code}")
print(f"Response: {resp.text[:800]}")

# Step 3: If update succeeded, get updated project
if resp.status_code == 200:
    print("\n--- Project updated successfully! ---")
    proj2 = resp.json()
    p = proj2.get("project", proj2)
    print(f"Name: {p.get('name')}")
    print(f"Status: {p.get('status')}")
    print(f"Repo: {p.get('repoLink')}")
    print(f"Demo: {p.get('technicalDemoLink')}")
    print(f"Tags: {p.get('tags')}")
    print(f"Description (first 200): {p.get('description', '')[:200]}")
