import os
import json

# ----------- Configuration -----------
INPUT_FOLDER = "../datas"
OUTPUT_FILE = "mega_data.json"

# ----------- Initialize merged data structure -----------
mega_users = {}

# ----------- Iterate through all JSON files in the input folder -----------
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        filepath = os.path.join(INPUT_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        source_id = str(data["source"])
        users = data["users"]

        # ----------- Merge users from current file into global structure -----------
        for user_id, user_data in users.items():
            if user_id not in mega_users:
                mega_users[user_id] = {
                    "name": user_data.get("name", ""),
                    "global_name": user_data.get("global_name", ""),
                    "avatar": user_data.get("avatar", ""),
                    "mutual": list(user_data.get("mutual", [])),
                    "sources": [source_id]
                }
            else:
                existing = mega_users[user_id]
                # Merge mutual connections (union of sets)
                existing["mutual"] = list(set(existing["mutual"]) | set(user_data.get("mutual", [])))
                if source_id not in existing["sources"]:
                    existing["sources"].append(source_id)

# ----------- Ensure cross-linking between users appearing in multiple sources -----------
for user_id, info in mega_users.items():
    if len(info["sources"]) > 1:
        for source_id in info["sources"]:
            if source_id != user_id and source_id not in info["mutual"]:
                info["mutual"].append(source_id)

# ----------- Save merged data to output JSON file -----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"users": mega_users}, f, indent=2, ensure_ascii=False)

print(f"✅ Mega file generated: {OUTPUT_FILE}")