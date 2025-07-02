[![Lang](https://img.shields.io/badge/lang-en-lightgrey.svg)](./README.md)
[![Lang](https://img.shields.io/badge/lang-fr-blue.svg)](./README.fr.md)

# 🧠 MutualMap

**Visualisez votre réseau d’amis Discord sous forme de graphe interactif — localement ou en combinant plusieurs jeux de données.**

---

## 🔍 Qu’est-ce que c’est ?

**MutualMap** est un ensemble d’outils permettant de générer des **graphes de réseau interactifs de vos amis Discord**, au format HTML.  
Chaque ami apparaît comme un nœud dans le graphe, et les liens représentent les relations mutuelles.  
Le graphe est visuel, en plein écran, coloré, et enrichi de statistiques en temps réel que l’on peut activer ou désactiver.

Vous pouvez :
- Visualiser **votre propre réseau d’amis**, ou
- Fusionner plusieurs exports pour créer un **graphe “méga” global** illustrant les connexions croisées entre utilisateurs

Aucun serveur, bot ou hébergement n’est nécessaire — tout fonctionne localement, dans votre navigateur.

---

## 🛠️ Comment l’utiliser ?

### Étape 1 – Exporter vos amis Discord

> ⚠️ Cette étape utilise votre token utilisateur Discord. C’est pratiquement sans risque (voir l’avertissement plus bas) si vous l’utilisez en privé et uniquement pour votre propre compte.

#### 🔐 Comment obtenir votre token Discord :

1. Ouvrez [https://discord.com](https://discord.com) dans **un navigateur sur ordinateur** (Chrome, Firefox…)
2. Connectez-vous à votre compte
3. Appuyez sur `F12` pour ouvrir les **outils de développement**
4. Allez dans l’onglet **Network (Réseau)**
5. Cliquez sur n’importe quelle **conversation privée**
6. Parmi les requêtes qui apparaissent, repérez celle nommée `messages?limit=50`
7. Cliquez dessus, puis allez dans l’onglet **Headers (En-têtes)**
8. Faites défiler jusqu’à trouver une clé appelée `Authorization` — c’est votre **token utilisateur**
9. Copiez-le et conservez-le en lieu sûr

> 🔴 Ne partagez jamais ce token. Traitez-le comme un mot de passe.
> Si vous craignez une fuite, changer votre mot de passe régénérera automatiquement le token.

#### 🧠 Utiliser le script :

1. Allez dans l’onglet **Console** des outils de développement
2. Collez le contenu complet du fichier [`getFriends.js`](getFriends.js)
3. Remplacez cette ligne :
   ```js
   const token = "YOUR_DISCORD_TOKEN_HERE";
   ```
   par votre token réel :
   ```js
   const token = "XXXXXXXXXXXXXXXXX";
   ```
4. Appuyez sur `Entrée` pour exécuter

Après quelques instants, un fichier nommé `friends_data.json` sera téléchargé automatiquement.

> ⏱️ Un délai d’une seconde entre chaque ami est ajouté pour limiter les appels à l’API.  
> Vous pouvez modifier ce délai dans le script (cherchez `setTimeout`), mais si vous n’êtes pas sûr·e, laissez la valeur par défaut.
> Pour environ 60 amis, l’export prend **un peu plus d’une minute**.

---

### Étape 2 – Où placer votre fichier JSON ?

- Si votre fichier se nomme `friends_data.json` et est placé **à la racine**, il sera **utilisé automatiquement** par le script Python.
- S’il a un autre nom ou s’il est placé dans `datas/`, le script vous demandera de le sélectionner manuellement.

> Vous pouvez répéter l’export pour d’autres comptes (secondaires, amis...) et renommer chaque fichier (`friends_data_alice.json`, `friends_data_bob.json`, etc.), puis les placer dans `datas/`.

---

### Étape 3 – Configurer Python

> ✅ Vous pouvez utiliser le terminal, ou double-cliquer sur les scripts si tout est bien installé.

1. [Installez Python](https://www.python.org/downloads/) (version 3.9 ou supérieure recommandée)
2. Ouvrez votre terminal et installez le paquet nécessaire :

```bash
pip install pyvis
```

- En cas d’erreur sur `pyvis`, vérifiez que Python est bien dans votre PATH.

---

### Étape 4 – Générer un graphe à partir d’un fichier

Pour créer un graphe à partir d’un seul fichier :

```bash
python generate_graph.py
```

- Si `friends_data.json` est à la racine, il sera utilisé.
- Sinon, le script vous demandera quel fichier choisir.
- Cela crée aussi les dossiers `/lib/` nécessaires si absents (pour les assets JS et CSS).
- Le résultat sera `discord_friends_network.html` à la racine.
- ⚠️ En relançant le script, le fichier HTML précédent sera **écrasé sans avertissement**.  
  ➤ Renommez ou déplacez vos anciens fichiers si besoin.

📂 Ce fichier peut être ouvert dans n’importe quel navigateur. Il contient les avatars, info-bulles et un panneau de stats.

---

### Étape 5 – Fusionner plusieurs fichiers en un graphe global

Si vous avez plusieurs fichiers `.json` dans `datas/`, vous pouvez générer une vue d’ensemble :

```bash
cd mega
python build_mega_data.py
python generate_mega_graph.py
```

- Les scripts sont dans le dossier `/mega`
- Le script de fusion crée `mega_data.json`
- Le script de graphes crée `mega_graph.html` avec les stats intégrées
- 📌 Les stats sont visibles dans un panneau que l’on peut afficher ou masquer

---

## 📊 Quelles statistiques sont affichées ?

Dans les graphes simples et méga, vous trouverez :

- Nombre total d’utilisateurs (nœuds)
- Nombre de connexions (liens)
- Densité du réseau (%)
- Moyenne et médiane d’amis communs
- Utilisateurs isolés + ratio
- Nombre de groupes connectés
- Taille du plus grand cluster
- Diamètre de ce cluster (nombre de sauts)
- Utilisateur le plus connecté dans ce cluster
- Top 3 des utilisateurs les plus connectés

Vous pouvez personnaliser l’apparence ou la langue dans `stats_box.html` ou `mega_stats_box.html`.

---

## 📁 Structure des fichiers

```
MutualMap/
│
├── getFriends.js             → Script JS pour exporter vos amis
├── generate_graph.py         → Génère un graphe pour un utilisateur
├── stats_box.html            → Panneau de stats pour les graphes simples
├── .gitignore                → Ignore certains dossiers comme /html/, /lib/, /datas/*
│
├── datas/                    → Placez vos fichiers .json ici
│
├── lib/                      → Fichiers JS/CSS (créés automatiquement si manquants)
│
└── mega/
    ├── build_mega_data.py         → Fusionne tous les fichiers de ../datas/
    ├── generate_mega_graph.py     → Génère un graphe complet avec stats
    ├── mega_data.json             → Données fusionnées auto-générées
    ├── mega_stats_box.html        → Template du panneau de stats
    └── lib/                       → JS/CSS pour accès autonome
```

❗ Le dossier `/datas/` n’est **pas fourni**. Créez-le et déposez vos fichiers `.json` pour utiliser les scripts du graphe global.

---

## ⚠️ Mention légale et sécurité

Ce projet repose sur votre **token utilisateur Discord**, qui donne accès à vos données. Bien que le script fasse uniquement des **opérations en lecture**, similaires à ce que le client web exécute :

- Il **n’envoie aucun message**
- Il **n’interagit pas avec d’autres utilisateurs ou serveurs**
- Il inclut un **délai intégré d’1 seconde** entre chaque appel à l’API
- Il s’exécute **dans votre navigateur**, connecté à votre compte
- Il **accède uniquement à des données peu sensibles**

🔐 Votre token doit rester **strictement privé**. Ne le partagez **jamais**. Ne le publiez pas sur GitHub, Discord, ou un drive. Cet outil est destiné à un **usage local et personnel uniquement**.

📎 L’usage d’un token pour des scripts est considéré comme un “selfbot” et **va à l’encontre des CGU de Discord**. Bien que cet outil soit passif, vous l’utilisez **à vos risques et périls**.

---

## 💡 Crédits & inspirations

- Basé sur l’idée originale de [fwendator par Escartem](https://github.com/Escartem/fwendator)  
- Amélioré avec des fonctionnalités : fusion de fichiers, stats intégrées, design visuel, refonte de l’architecture
- Visualisation assurée par [PyVis](https://pyvis.readthedocs.io/) et [Vis.js](https://visjs.org/)
- Interface, logique et intégration assurées par le mainteneur actuel
- Conçu avec 🧠 clarté et 🍵 bon thé
- Fait par un ami, pour les amis 💙

---

## 🧩 Idées pour l’avenir

- Filtrer les nœuds selon le nombre d’amis en commun
- Colorer les clusters ou groupes d’amis
- Exporter les graphes en image (PNG, SVG)
- Suivre l’évolution du graphe dans le temps
