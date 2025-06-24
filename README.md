# 🧠 MutualMap
**Visualize your Discord friend network as a beautiful interactive graph.**

---

## 🔍 What is it?

**MutualMap** is a small project that lets you generate an **interactive network graph of your Discord friends**, showing how your contacts are connected to each other (mutual friends).  

The project consists of:
- A small **JavaScript script** that fetches your Discord friends and their mutual connections.
- A **Python visualization tool** that builds and exports the graph as an interactive **HTML file**.

You’ll get something like this:  
➡️ A full-screen network graph where each node is one of your friends. The more mutuals they have, the bigger and redder they appear.

---

## 🛠️ How to use it?

### Step 1 – Get your Discord token (browser)

> ⚠️ This process **only works on desktop browsers** (like Chrome, Edge or Firefox).
> You **cannot** use the mobile app or desktop Discord client.

1. Go to [https://discord.com](https://discord.com) and **log into your account**  
2. Press `F12` or `Ctrl + Shift + I` to open **Developer Tools**
3. Go to the **Network** tab  
4. In Discord, click on **any friend’s conversation**
5. In the list of network requests, **look for something like** `messages?limit=50`  
6. Click on it, then go to the **"Headers"** tab
7. Scroll down until you find a line called **`Authorization`**
8. The value next to it is your **user token** (a long string)  
   → Copy it somewhere **but keep it secret** ⚠️

---

### Step 2 – Use the JavaScript file to fetch your friend network

1. Open a browser tab on [https://discord.com](https://discord.com)
2. Press `F12` to open Developer Tools again
3. Go to the **Console** tab
4. Paste the content of the `getFriends.js` file (or drag and drop it into the console)
5. Replace the line:
   ```js
   const token = "YOUR_DISCORD_TOKEN_HERE";
   ```
   with:
   ```js
   const token = "XXXXXXXXXM1512XXX";
   ```

6. Press `Enter` to run it
7. Wait. It may take a few minutes depending on how many friends you have.
8. When it's done, your browser will download a file named **`friends_data.json`**

---

### Step 3 – Generate the graph (Python)

1. Make sure you have Python installed (Python 3.9+ recommended)
2. Install the required package:

```bash
pip install pyvis
```

3. Run the script:

```bash
python generate_graph.py
```

4. If the JSON file is named differently, you will be prompted to select it.
5. After a few seconds, a file called **`discord_friends_network.html`** will be created.
6. Open it in your browser and explore your friend network 🎉

---

## ⚠️ Legal & ethical notice

> ❌ This script is technically a **self-bot**.  
> It uses your user token and mimics API calls made by Discord’s front-end.

**Discord’s terms of service forbid self-bots**, and using one *irresponsibly* (e.g. sending messages, automating moderation, joining/leaving servers, etc.) **can result in a ban**.

However, this tool:
- **Does not send messages**
- **Does not interact with other users**
- **Only mimics safe read-only front-end behavior**

🟢 **If you follow the instructions and use the browser console as shown, the risk is extremely low.**

Still, do this **at your own discretion**, and never share your token with anyone.

---

## 📁 File structure

```
MutualMap/
│
├── getFriends.js            → Fetches your friend list and mutual connections
├── generate_graph.py        → Builds the HTML network visualization
├── friends_data.json        → Your exported data file (auto-generated)
└── discord_friends_network.html → The final result (auto-generated)
```

---

## 💡 Credits & ideas

- Inspired by [Escartem's fwendator](https://github.com/Escartem/fwendator), a similar Discord friend graphing project
- Powered by **PyVis** (based on Vis.js)
- Inspired by the idea of “mutual networks” in social graphs
- Made with curiosity and caffeine ☕

---

## 🧩 Next ideas

- Add a filter by mutual count
- Allow export as PNG (tricky with avatars!)
- Add usernames on hover + link to Discord profiles
