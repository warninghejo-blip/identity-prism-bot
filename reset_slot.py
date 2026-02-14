import json
with open("/opt/identityprism-bot/state.json") as f:
    s = json.load(f)
s["last_slot_at"] = 0
with open("/opt/identityprism-bot/state.json", "w") as f:
    json.dump(s, f, indent=2)
print("Reset last_slot_at to 0")
