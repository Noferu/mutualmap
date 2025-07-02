// 🚨 Replace this with your actual Discord user token
const token = "YOUR_DISCORD_TOKEN_HERE";

/**
 * Authenticated fetch call with your token.
 */
async function fetchWithAuth(url, token) {
  const response = await fetch(url, {
    headers: { Authorization: token }
  });
  return await response.json();
}

/**
 * Fetches only real friends (type === 1) with their mutuals.
 */
async function getFriends(token) {
  console.log("📡 Connecting to Discord...");

  // Get your own user info
  const me = await fetchWithAuth("https://discord.com/api/v9/users/@me", token);

  const result = {
    source: me.id,
    users: {}
  };

  console.log("👤 Exporting as:", `${me.username}#${me.discriminator}`);

  // Get relationships and filter only type === 1 (friends)
  const relationships = await fetchWithAuth("https://discord.com/api/v9/users/@me/relationships", token);
  const friendsOnly = relationships.filter(rel => rel.type === 1); // Only real friends

  for (const rel of friendsOnly) {
    const friend = rel.user;

    // Try to fetch mutuals (optional step)
    const mutualIds = await fetchWithAuth(
      `https://discord.com/api/v9/users/${friend.id}/relationships`,
      token
    ).then(res => res.map(u => u.id)).catch(() => []);

    result.users[friend.id] = {
      name: `${friend.username}#${friend.discriminator}`,
      global_name: friend.global_name || "",
      avatar: friend.avatar || "",
      mutual: mutualIds
    };

    console.log(`✅ Fetched: ${friend.username}`);
    await new Promise(resolve => setTimeout(resolve, 1000)); // prevent rate limit
  }

  // Trigger file download
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "friends_data.json";
  a.click();
  URL.revokeObjectURL(url);

  console.log("📁 Saved as: friends_data.json");
}

// Launch
getFriends(token);
