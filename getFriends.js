// 🚨 Replace this with your actual Discord user token
const token = "YOUR_DISCORD_TOKEN_HERE";

/**
 * Authenticated fetch call with your token.
 * Used to call Discord's private API endpoints.
 */
async function fetchWithAuth(url, token) {
  const response = await fetch(url, {
    headers: { Authorization: token }
  });
  return await response.json();
}

/**
 * Fetches your own user info and your friend list with mutual connections.
 * Exports the data as a JSON file.
 */
async function getFriends(token) {
  console.log("📡 Connecting to Discord...");

  // Get the current user's account info (you, the source)
  const me = await fetchWithAuth("https://discord.com/api/v9/users/@me", token);

  // Initialize result with your user ID as the source
  const result = {
    source: me.id, // just the ID of the person exporting this data
    users: {}      // where friends will be stored
  };

  console.log("👤 Exporting as:", `${me.username}#${me.discriminator}`);

  // Get your full friends list (one-way and mutual)
  const relationships = await fetchWithAuth("https://discord.com/api/v9/users/@me/relationships", token);

  for (const rel of relationships) {
    const friend = rel.user;

    // Get their relationships (used to determine mutuals)
    const mutualIds = await fetchWithAuth(
      `https://discord.com/api/v9/users/${friend.id}/relationships`,
      token
    ).then(res => res.map(u => u.id)).catch(() => []); // ignore errors

    // Store the user's data in the final object
    result.users[friend.id] = {
      name: `${friend.username}#${friend.discriminator}`,
      global_name: friend.global_name || "",
      avatar: friend.avatar || "",
      mutual: mutualIds // list of user IDs that are mutual with this friend
    };

    console.log(`✅ Fetched: ${friend.username}`);
    await new Promise(resolve => setTimeout(resolve, 1000)); // avoid rate limits
  }

  // Convert data to JSON and trigger file download
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "friends_data.json";
  a.click();
  URL.revokeObjectURL(url);

  console.log("📁 Saved as: friends_data.json");
}

// Run the export process
getFriends(token);