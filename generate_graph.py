import json
from pyvis.network import Network
import os
from tkinter import Tk, filedialog
from collections import defaultdict, deque
import statistics

# ----------- File selection -----------
default_file = "friends_data.json"

if not os.path.exists(default_file):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select your JSON file", filetypes=[("JSON files", "*.json")])
    if not file_path:
        raise FileNotFoundError("No file selected.")
else:
    file_path = default_file

print(f"📄 Loaded file: {file_path}")

# ----------- Load JSON data -----------
with open(file_path, "r", encoding="utf-8") as file:
    content = json.load(file)

all_data = content["users"]

# ----------- Ask which relation types to include -----------
print("\nWhich relationship types would you like to include?")
print("1 = Friends, 2 = Blocked, 3 = Outgoing Requests, 4 = Incoming Requests")
selected = input("Enter the types you want to include (comma separated, e.g. 1,4): ")
allowed_types = set(map(int, selected.split(",")))

# ----------- Filter users by selected relationship types -----------
data = {uid: info for uid, info in all_data.items() if info.get("relation_type") in allowed_types}

# ----------- Initialize network graph -----------
net = Network(height="100vh", width="100vw", bgcolor="#1e1e1e", font_color="white")
net.force_atlas_2based()

# ----------- Styling helper -----------
def style_for_node(n_relations):
    base_size = 12
    size = min(50, base_size + n_relations * 5)
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
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{info['avatar']}.png?size=64" if info.get("avatar") else "https://cdn.discordapp.com/embed/avatars/0.png"
    net.add_node(user_id, label=display_name, title=info["name"], shape="circularImage", image=avatar_url, size=size, color=color)

# ----------- Add edges -----------
edges_added = set()
adjacency = defaultdict(set)
for user_id, info in data.items():
    for mutual_id in info["mutual"]:
        if mutual_id in data and (mutual_id, user_id) not in edges_added:
            net.add_edge(user_id, mutual_id, width=2.5)
            edges_added.add((user_id, mutual_id))
            adjacency[user_id].add(mutual_id)
            adjacency[mutual_id].add(user_id)

# ----------- Compute stats -----------
total_nodes = len(data)
total_edges = len(edges_added)
average_degree = (2 * total_edges) / total_nodes if total_nodes > 0 else 0
density = (2 * total_edges) / (total_nodes * (total_nodes - 1)) * 100 if total_nodes > 1 else 0
isolated_users = [uid for uid, info in data.items() if not info["mutual"]]
isolated_ratio = len(isolated_users) / total_nodes * 100 if total_nodes else 0

centrality_scores = {uid: len(info["mutual"]) / (total_nodes - 1) if total_nodes > 1 else 0 for uid, info in data.items()}
top_central_info = sorted(((uid, centrality_scores[uid], len(data[uid]["mutual"])) for uid in data), key=lambda x: x[1], reverse=True)[:3]

def get_connected_components(adj):
    visited = set()
    components = []
    for node in adj:
        if node not in visited:
            queue = deque([node])
            component = []
            while queue:
                current = queue.popleft()
                if current not in visited:
                    visited.add(current)
                    component.append(current)
                    queue.extend(adj[current] - visited)
            components.append(component)
    return components

components = get_connected_components(adjacency)
component_sizes = [len(c) for c in components]
average_component_size = statistics.mean(component_sizes) if component_sizes else 0

largest_cluster = max(components, key=len) if components else []
largest_cluster_size = len(largest_cluster)
cluster_degrees = {uid: len(data[uid]["mutual"]) for uid in largest_cluster}
top_user_cluster_id = max(cluster_degrees.items(), key=lambda x: x[1])[0] if cluster_degrees else ""
top_user_cluster_degree = cluster_degrees.get(top_user_cluster_id, 0)
top_user_cluster_centrality = top_user_cluster_degree / (largest_cluster_size - 1) * 100 if largest_cluster_size > 1 else 0
top_user_cluster_name = data[top_user_cluster_id].get("global_name") if top_user_cluster_id in data else "N/A"

# ----------- Export HTML -----------
output_file = "discord_friends_network.html"
net.show(output_file)

# ----------- Inject stats into HTML -----------
with open("stats_box.html", "r", encoding="utf-8") as f:
    template = f.read()

central_html = "".join(
    f"<li>{data[uid].get('global_name') or data[uid]['name']} "
    f"<span style='color:gray;'>({degree} connections, {score * 100:.1f}%)</span></li>"
    for uid, score, degree in top_central_info
)
central_block = f"<ul>{central_html}</ul>"

stats_html = (
    template
    .replace("{total_nodes}", str(total_nodes))
    .replace("{total_edges}", str(total_edges))
    .replace("{density}", f"{density:.1f}")
    .replace("{average_degree}", f"{average_degree:.1f}")
    .replace("{isolated_users}", str(len(isolated_users)))
    .replace("{isolated_ratio}", f"{isolated_ratio:.1f}")
    .replace("{connected_components}", str(len(components)))
    .replace("{average_component_size}", f"{average_component_size:.1f}")
    .replace("{largest_cluster_size}", str(largest_cluster_size))
    .replace("{top_cluster_user}", top_user_cluster_name)
    .replace("{top_cluster_centrality}", f"{top_user_cluster_centrality:.1f}")
    .replace("{top_influencers}", central_block)
)

with open(output_file, "r", encoding="utf-8") as f:
    html_content = f.read()

html_content = html_content.replace("<body>", f"<body>\n{stats_html}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Graph successfully generated.")
