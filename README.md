# 🧠 MutualMap

**Visualize your Discord friend network as an interactive graph – locally, or across multiple datasets.**

---

## 🔍 What is it?

**MutualMap** is a toolset that lets you generate **interactive network graphs of your Discord friends** in HTML format.  
Each friend appears as a node in the graph, and links represent mutual relationships.  
The graph is visual, full-screen, color-coded, and enriched with real-time stats you can toggle on or off.

You can either:
- Visualize your **own personal friend network**, or
- Merge multiple exported datasets into a **global “mega” graph** that shows cross-user connections

No need for servers, bots or hosting — everything is done locally in your browser.

---

## 🛠️ How to use it?

### Step 1 – Export your Discord friends

> ⚠️ This step uses your Discord user token. It’s safe if used privately and only for your own account.

#### 🔐 How to get your Discord token:

1. Open [https://discord.com](https://discord.com) in **a desktop browser** (Chrome, Firefox…)
2. Log into your account
3. Press `F12` to open the **Developer Tools**
4. Go to the **Network** tab
5. Click on any **DM with a friend**
6. In the requests that appear, look for one named `messages?limit=50`
7. Click on it, then go to the **Headers** tab
8. Scroll down to find a key called `authorization` — this is your **user token**
9. Copy it and paste it somewhere safe

> 🔴 Never share this token. Treat it like a password.

#### 🧠 Use the script:

1. Go to the **Console** tab in Developer Tools
2. Paste the full content of `getFriends.js`
3. Replace this line:
   ```js
   const token = "YOUR_DISCORD_TOKEN_HERE";
   ```
   with your actual token:
   ```js
   const token = "mfa.XXXXXXXXXXXXXXX";
   ```
4. Press `Enter` to run it

After a short wait, a file named `friends_data.json` will be automatically downloaded.

> ⏱️ A 1-second delay between each friend is added to reduce API spam and stay safe.  
> You can adjust the delay in the script (look for `setTimeout`).  
> With ~60 friends, the export should take **a bit more than one minute**.

---

### Step 2 – Where to put your JSON file?

- If your file is named `friends_data.json` and placed **in the root folder**, it will be **used automatically** by the Python script.
- If it has a different name, or if you place it in the `datas/` folder, the script will ask you to select the file manually.
- ⚠️ If you run the script again, it will **overwrite any previous HTML file without warning**.  
  ➤ Rename or move your outputs as needed to avoid accidental overwrites.

> You can repeat the export step for other accounts (alts, friends...) and rename each file like `friends_data_alice.json`, `friends_data_bob.json`, etc., and place them all in `datas/`.

---

### Step 3 – Set up Python

> ✅ You can use the terminal, or just double-click the Python scripts if everything is correctly installed.

1. [Install Python](https://www.python.org/downloads/) (version 3.9+ recommended)
2. Open your terminal and install required packages:

```bash
pip install pyvis
```

- This will also create the necessary `/lib/` folders if they don’t exist yet (for JavaScript and CSS assets).
- If you see errors about `pyvis` not being found, make sure you added Python to your PATH.

---

### Step 4 – Generate a graph from one file

To create a graph from a single dataset:

```bash
python generate_graph.py
```

- If `friends_data.json` is in the root, it will be used.
- Otherwise, you’ll be prompted to choose your file.
- The result is `discord_friends_network.html` in the root.

📂 This file can be opened in any browser. It includes avatars, tooltips, and a stats panel.

---

### Step 5 – Merge multiple files into one mega graph

If you’ve gathered multiple `.json` exports and placed them in `datas/`, you can create a full overview:

```bash
cd mega
python build_mega_data.py
python generate_mega_graph.py
```

- The merging script will create `mega_data.json` in `/mega/`
- The graph script will generate `mega_graph.html` with stats injected
- 📌 Stats are shown in a toggleable panel on the graph

---

## 📊 What kind of stats are shown?

In both normal and mega graphs, you'll find:

- Total users (nodes)
- Total connections (edges)
- Network density (%)
- Average and median number of mutuals
- Isolated users + ratio
- Number of connected groups
- Size of the biggest cluster
- Diameter of that cluster (max hops)
- Most connected user in that group
- Top 3 most connected users overall

You can customize the layout or language in `stats_box.html` or `mega_stats_box.html`.

---

## 📁 File structure

```
MutualMap/
│
├── getFriends.js             → JavaScript to export Discord friends
├── generate_graph.py         → Graph generator for one user
├── stats_box.html            → Stats panel for single-user graphs
├── .gitignore                → Ignores folders like /html/, /lib/, /datas/*
│
├── datas/                    → Put your .json files here (folder is empty by default)
│
├── lib/                      → JS/CSS assets (auto-created if missing)
│
└── mega/
    ├── build_mega_data.py         → Merge all files in ../datas/
    ├── generate_mega_graph.py     → Graph builder with rich stats
    ├── mega_data.json             → Auto-generated merged data
    ├── mega_stats_box.html        → Stats panel template
    └── lib/                       → JS/CSS for standalone access
```

❗ The `/html/` folders are **not provided**. Output HTML files are generated dynamically by the scripts in corresponding folders.

---

## ⚠️ Legal & safety notice

This project relies on your personal Discord **user token**, which gives access to your account data. While the script only performs **read-only operations** that mimic what the web client does:

- It **does not send messages**
- It **does not interact with users or servers**
- It includes a built-in **1-second delay between each API call** to avoid spamming and reduce risk

🔐 Your token must remain **strictly private**. Do **not** share it with anyone. Do **not** upload it to GitHub, Discord, or cloud drives. This tool is designed for **local and personal use only**.

📎 Using a user token for automated scripts is considered a “selfbot” and is **against Discord’s Terms of Service**. While this tool is passive and non-intrusive, you use it **at your own risk**.

---

## 💡 Credits & inspiration

- Based on the original idea and foundation from [Escartem's fwendator](https://github.com/Escartem/fwendator) 💙  
- Improved with custom features: merging support, toggleable stat panels, visual styling, and file structure refactoring
- Visualization powered by [PyVis](https://pyvis.readthedocs.io/) and [Vis.js](https://visjs.org/)
- UI, logic and integration by the current maintainer
- Built with 🧠 clarity and 🍵 good Moroccan tea

---

## 🧩 Future ideas

- Filter nodes by number of mutuals
- Color-code clusters or friend groups
- Export graphs as images (PNG, SVG)
- Track how the graph evolves over time