"""Update project via PUT /api/my-project with correct limits."""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets = json.loads(Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json").read_text())
api_key = secrets["apiKey"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Description must be <= 1000 chars, tags <= 3
description = (
    "Identity Prism — on-chain reputation & identity layer for Solana. "
    "Connect any wallet: get reputation score (0-1400), celestial tier, badges, 3D identity card from real on-chain data.\n\n"
    "Features:\n"
    "- Public Reputation API: /api/reputation?address=WALLET — trust scoring, sybil detection\n"
    "- On-Chain Attestation via Solana Memo Program, co-signed by authority. Works as Blink.\n"
    "- Verify page: identityprism.xyz/verify\n"
    "- AI Twitter Agent (@Identity_Prism): wallet auto-reply, threads, AI images (Gemini Imagen)\n"
    "- 3D Solar System: planets=tokens, moons=NFTs (Three.js)\n"
    "- 14 scoring factors, 13 badges, 10 celestial tiers\n"
    "- Solana Blinks/Actions: share card, mint NFT, attest reputation\n"
    "- cNFT via Metaplex Core, Black Hole token burner, Android app\n\n"
    "Stack: Vite+React+Three.js, Helius DAS, Gemini AI, Metaplex Core, Solana Memo, Capacitor\n"
    "Live: https://identityprism.xyz"
)
print(f"Description length: {len(description)} chars")
assert len(description) <= 1000, f"Too long: {len(description)}"

solana_integration = (
    "1. Helius RPC+DAS API: tx history, tokens, NFTs → 14-factor reputation scoring\n"
    "2. Solana Memo Program: on-chain attestation — JSON memo co-signed by treasury keypair\n"
    "3. Metaplex Core: mint identity cards as on-chain NFTs with collection verification\n"
    "4. SPL Token: SOL payments, token balance analysis for scoring\n"
    "5. Solana Actions/Blinks: share card, mint NFT, attest reputation — Phantom/Backpack/Dialect\n"
    "6. Black Hole: burns SPL tokens (TOKEN_PROGRAM+TOKEN_2022), reclaims rent\n"
    "7. Reputation API: public REST — any dApp can assess wallet trust or detect sybils"
)

update_payload = {
    "description": description,
    "repoLink": "https://github.com/YourIdentityPrism/identity-prism",
    "solanaIntegration": solana_integration,
    "technicalDemoLink": "https://identityprism.xyz",
    "tags": ["ai", "identity", "consumer"],
}

resp = r.put("https://agents.colosseum.com/api/my-project", headers=headers,
             json=update_payload, impersonate="chrome131", timeout=30)
print(f"PUT /api/my-project: {resp.status_code}")
print(f"Response: {resp.text[:800]}")

if resp.status_code == 200:
    p = resp.json().get("project", resp.json())
    print(f"\n=== SUCCESS ===")
    print(f"Name: {p.get('name')}")
    print(f"Status: {p.get('status')}")
    print(f"Repo: {p.get('repoLink')}")
    print(f"Demo: {p.get('technicalDemoLink')}")
    print(f"Tags: {p.get('tags')}")
