"""Fix badge count and fetch all projects for analysis."""
import json
from pathlib import Path
from curl_cffi import requests as r

secrets = json.loads(Path("/opt/identityprism-bot/secrets/colosseum-hackathon.json").read_text())
headers = {"Authorization": f"Bearer {secrets['apiKey']}", "Content-Type": "application/json"}

# 1. Try to fix description after submit
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
resp = r.put("https://agents.colosseum.com/api/my-project", headers=headers,
             json={"description": fixed_desc}, impersonate="chrome131", timeout=30)
print(f"FIX description: {resp.status_code} — {resp.text[:200]}")

# 2. Fetch ALL projects (submitted + drafts)
all_projects = []
for include_drafts in [False, True]:
    url = "https://agents.colosseum.com/api/projects/current"
    if include_drafts:
        url += "?includeDrafts=true"
    resp = r.get(url, impersonate="chrome131", timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        projects = data if isinstance(data, list) else data.get("projects", data.get("data", []))
        print(f"\nProjects (drafts={include_drafts}): {len(projects)}")
        if include_drafts:
            all_projects = projects
        else:
            if not all_projects:
                all_projects = projects

# 3. Fetch leaderboard
resp = r.get("https://agents.colosseum.com/api/leaderboard", impersonate="chrome131", timeout=30)
print(f"\nLeaderboard: {resp.status_code}")
if resp.status_code == 200:
    lb = resp.json()
    lb_list = lb if isinstance(lb, list) else lb.get("leaderboard", lb.get("data", []))
    print(f"Leaderboard entries: {len(lb_list)}")
    for entry in lb_list[:20]:
        name = entry.get("name", entry.get("agentName", "?"))
        score = entry.get("score", entry.get("points", "?"))
        print(f"  {name}: {score}")

# 4. Print all projects with details
print(f"\n{'='*80}")
print(f"TOTAL PROJECTS: {len(all_projects)}")
print(f"{'='*80}")
for p in sorted(all_projects, key=lambda x: x.get("humanUpvotes", 0) + x.get("agentUpvotes", 0), reverse=True):
    name = p.get("name", "?")
    status = p.get("status", "?")
    human_votes = p.get("humanUpvotes", 0)
    agent_votes = p.get("agentUpvotes", 0)
    tags = p.get("tags", [])
    repo = p.get("repoLink", "")
    demo = p.get("technicalDemoLink", "")
    video = p.get("presentationLink", "")
    desc = (p.get("description", "") or "")[:150]
    solana = (p.get("solanaIntegration", "") or "")[:100]
    print(f"\n--- {name} [{status}] ---")
    print(f"  Votes: human={human_votes}, agent={agent_votes}, total={human_votes+agent_votes}")
    print(f"  Tags: {tags}")
    print(f"  Repo: {repo}")
    print(f"  Demo: {demo}")
    print(f"  Video: {video}")
    print(f"  Desc: {desc}")
    print(f"  Solana: {solana}")
