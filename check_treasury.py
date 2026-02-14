import json, os
keys_dir = "/opt/identityprism/helius-proxy/keys"
for f in os.listdir(keys_dir):
    fp = os.path.join(keys_dir, f)
    try:
        d = json.load(open(fp))
        print(f"{f}: type={type(d).__name__}, len={len(d) if isinstance(d, list) else 'N/A'}")
    except:
        print(f"{f}: not JSON")

# Check if COLLECTION_AUTHORITY_SECRET is set
env_file = "/opt/identityprism/helius-proxy/.env"
for line in open(env_file):
    if "COLLECTION_AUTHORITY_SECRET" in line or "TREASURY_SECRET" in line:
        key = line.split("=")[0].strip()
        val = line.split("=", 1)[1].strip() if "=" in line else ""
        print(f"{key}: {'SET' if val else 'EMPTY'} ({len(val)} chars)")
