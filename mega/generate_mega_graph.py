import json
from pyvis.network import Network
import os
from collections import defaultdict, deque
import statistics

# ----------- Configuration -----------
EXCLUDE_ZERO_MUTUALS = True
file_path = "mega_data.json"
output_file = "mega_graph.html"
stats_template = "mega_stats_box.html"

# ----------- Load JSON data -----------
if not os.path.exists(file_path):
    raise FileNotFoundError("❌ mega_data.json not found.")

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

users = data.get("users", {})

# ----------- Initialize graph with visual options -----------
net = Network(height="100vh", width="100vw", bgcolor="#1e1e1e", font_color="white")
net.force_atlas_2based()

net.set_options("""var options = {
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -150,
      "centralGravity": 0.003,
      "springLength": 160,
      "springConstant": 0.08,
      "damping": 0.4,
      "avoidOverlap": 2
    },
    "minVelocity": 0.5,
    "solver": "forceAtlas2Based",
    "timestep": 0.5,
    "stabilization": {
      "iterations": 200,
      "fit": true
    }
  },
  "edges": {
    "color": {
      "color": "#990000",
      "highlight": "#ffffff",
      "hover": "#ffffff"
    },
    "width": 1.5,
    "hoverWidth": 4,
    "selectionWidth": 5,
    "smooth": {
      "enabled": true,
      "type": "continuous"
    }
  },
  "interaction": {
    "hover": true,
    "hoverConnectedEdges": true,
    "selectConnectedEdges": true
  },
  "nodes": {
    "font": {
      "size": 24
    },
    "scaling": {
      "min": 24,
      "max": 90
    },
    "color": {
      "highlight": {
        "border": "#ffffff",
        "background": "#ffffff"
      },
      "hover": {
        "border": "#ffffff",
        "background": "#ffffff"
      }
    }
  }
}""")

# ----------- Node styling helper -----------
def style_for_node(n_relations, max_relations, min_size=24, max_size=90):
    ratio = n_relations / max_relations if max_relations > 0 else 0
    size = min_size + (max_size - min_size) * ratio
    red = min(255, 80 + n_relations * 15)
    green = max(0, 100 - n_relations * 5)
    blue = max(0, 100 - n_relations * 5)
    color = f"rgb({int(red)},{int(green)},{int(blue)})"
    return size, color

# ----------- Add nodes to the graph -----------
max_relations = max((len(info.get("mutual", [])) for info in users.values() if info.get("mutual")), default=1)

for user_id, info in users.items():
    mutuals = info.get("mutual", [])
    if EXCLUDE_ZERO_MUTUALS and not mutuals:
        continue
    display_name = info.get("global_name") or info.get("name", "unknown").split("#")[0]
    size, color = style_for_node(len(mutuals), max_relations)
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{info['avatar']}.png?size=64" if info.get("avatar") else "https://cdn.discordapp.com/embed/avatars/0.png"
    net.add_node(user_id, label=display_name, title=info.get("name", ""), shape="circularImage", image=avatar_url, size=size, color=color)

# ----------- Add edges between mutual friends -----------
edges_added = set()
adjacency = defaultdict(set)

for user_id, info in users.items():
    if EXCLUDE_ZERO_MUTUALS and not info.get("mutual"):
        continue
    for mutual_id in info.get("mutual", []):
        if mutual_id in users and (mutual_id, user_id) not in edges_added:
            if EXCLUDE_ZERO_MUTUALS and not users[mutual_id].get("mutual"):
                continue
            net.add_edge(user_id, mutual_id, width=2.5)
            edges_added.add((user_id, mutual_id))
            adjacency[user_id].add(mutual_id)
            adjacency[mutual_id].add(user_id)

net.write_html(output_file)

# ----------- Compute general statistics -----------
total_nodes = len(users)
total_edges = len(edges_added)
degrees = [len(info.get("mutual", [])) for info in users.values()]
average_degree = (2 * total_edges) / total_nodes if total_nodes > 0 else 0
median_degree = statistics.median(degrees) if degrees else 0
std_degree = statistics.stdev(degrees) if len(degrees) > 1 else 0
density = (2 * total_edges) / (total_nodes * (total_nodes - 1)) * 100 if total_nodes > 1 else 0
isolated_users = [uid for uid, info in users.items() if not info.get("mutual")]
isolated_ratio = len(isolated_users) / total_nodes * 100 if total_nodes else 0

# ----------- Identify connected components -----------
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
largest_cluster = max(components, key=len)
largest_cluster_size = len(largest_cluster)
large_components_count = sum(1 for c in components if len(c) > 10)

# ----------- Compute diameter of the largest cluster -----------
def cluster_diameter(cluster):
    max_d = 0
    for node in cluster:
        visited = {node: 0}
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in cluster and neighbor not in visited:
                    visited[neighbor] = visited[current] + 1
                    queue.append(neighbor)
        max_d = max(max_d, max(visited.values(), default=0))
    return max_d

largest_cluster_diameter = cluster_diameter(set(largest_cluster))

# ----------- Compute centrality scores and top users -----------
centrality_scores = {uid: len(info["mutual"]) / (total_nodes - 1) if total_nodes > 1 else 0 for uid, info in users.items()}
top_central_info = sorted(((uid, centrality_scores[uid], len(users[uid]["mutual"])) for uid in users), key=lambda x: x[1], reverse=True)[:10]

top_user_cluster_id = max(largest_cluster, key=lambda uid: len(users[uid]["mutual"]))
top_user_cluster_name = users[top_user_cluster_id].get("global_name") or users[top_user_cluster_id]["name"]
top_user_cluster_centrality = len(users[top_user_cluster_id]["mutual"]) / (largest_cluster_size - 1) * 100 if largest_cluster_size > 1 else 0

# ----------- Generate HTML block for top influencers -----------
top_influencers_html = "".join(
    f"<li>{users[uid].get('global_name') or users[uid]['name']} "
    f"<span style='color:gray;'>({degree} connections, {score * 100:.1f}%)</span></li>"
    for uid, score, degree in top_central_info
)
top_influencers_block = f"<ul>{top_influencers_html}</ul>"

# ----------- Inject statistics into HTML template -----------
with open(stats_template, "r", encoding="utf-8") as f:
    template = f.read()

html_stats = (
    template
    .replace("{total_nodes}", str(total_nodes))
    .replace("{total_edges}", str(total_edges))
    .replace("{density}", f"{density:.1f}")
    .replace("{average_degree}", f"{average_degree:.1f}")
    .replace("{median_degree}", f"{median_degree:.1f}")
    .replace("{std_degree}", f"{std_degree:.1f}")
    .replace("{isolated_users}", str(len(isolated_users)))
    .replace("{isolated_ratio}", f"{isolated_ratio:.1f}")
    .replace("{connected_components}", str(len(components)))
    .replace("{large_components_count}", str(large_components_count))
    .replace("{average_component_size}", f"{average_component_size:.1f}")
    .replace("{largest_cluster_size}", str(largest_cluster_size))
    .replace("{largest_cluster_diameter}", str(largest_cluster_diameter))
    .replace("{top_cluster_user}", top_user_cluster_name)
    .replace("{top_cluster_centrality}", f"{top_user_cluster_centrality:.1f}")
    .replace("{top_influencers}", top_influencers_block)
)

with open(output_file, "r", encoding="utf-8") as f:
    html_content = f.read()

html_content = html_content.replace("<body>", "<body>\n" + html_stats)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Enriched graph with statistics generated in mega_graph.html")