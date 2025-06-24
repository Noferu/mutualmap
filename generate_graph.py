import json
from pyvis.network import Network
import os
from tkinter import Tk, filedialog

# ----------- File selection -----------

# Set default file name (you can rename or leave blank to force prompt)
default_file = "friends_data.json"

# Prompt file selection if default doesn't exist
if not os.path.exists(default_file):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your JSON file",
        filetypes=[("JSON files", "*.json")]
    )
    if not file_path:
        raise FileNotFoundError("No file selected.")
else:
    file_path = default_file

# ----------- Load JSON data -----------

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# ----------- Initialize network graph -----------

# Create a full-screen dark-themed network
net = Network(height="100vh", width="100vw", bgcolor="#1e1e1e", font_color="white")

# Enable ForceAtlas2 layout algorithm for better clustering
net.force_atlas_2based()

# ----------- Styling helper function -----------

def style_for_node(n_relations):
    """Return size and color based on number of mutual relations."""
    base_size = 12
    size = min(50, base_size + n_relations * 4)
    red = min(255, 80 + n_relations * 15)
    green = max(0, 100 - n_relations * 5)
    blue = max(0, 100 - n_relations * 5)
    color = f"rgb({red},{green},{blue})"
    return size, color

# ----------- Add nodes -----------

for user_id, info in data.items():
    display_name = info.get("global_name") or info["name"].split("#")[0]
    relation_count = len(info["mutual"])
    size, color = style_for_node(relation_count)

    # Use avatar if available, fallback to default placeholder
    avatar_url = (
        f"https://cdn.discordapp.com/avatars/{user_id}/{info['avatar']}.png?size=64"
        if info.get("avatar")
        else "https://cdn.discordapp.com/embed/avatars/0.png"
    )

    net.add_node(
        user_id,
        label=display_name,
        title=info["name"],  # full username (e.g. Example#1234)
        shape="circularImage",
        image=avatar_url,
        size=size,
        color=color,
    )

# ----------- Add edges (connections) -----------

edges_added = set()

for user_id, info in data.items():
    for mutual_id in info["mutual"]:
        # Avoid duplicate edges by checking both directions
        if mutual_id in data and (mutual_id, user_id) not in edges_added:
            net.add_edge(user_id, mutual_id, width=2.5)  # Thicker edge
            edges_added.add((user_id, mutual_id))

# ----------- Export the network to an HTML file -----------

output_file = "discord_friends_network.html"
net.show(output_file)

print(f"✅ Network graph successfully generated.")
print(f"📂 Open '{output_file}' in your browser to view the interactive graph.")