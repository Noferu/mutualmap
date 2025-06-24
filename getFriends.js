// 🚨 Replace this with your actual Discord user token
const token = "YOUR_DISCORD_TOKEN_HERE";

/**
 * Generic fetch wrapper with token authentication.
 * @param {string} url - The API endpoint.
 * @param {string} token - Discord token for authorization.
 * @returns {Promise<object>} - JSON response.
 */
async function fetchWithAuth(url, token) {
  const response = await fetch(url, {
    headers: { Authorization: token }
  });
  return await response.json();
}

/**
 * Retrieves the friend list and mutual connections from Discord.
 * Saves the result as a JSON file.
 * @param {string} token - Your Discord user token.
 */
async function getFriends(token) {
  console.log("📡 Fetching your friend list...");

  const relationships = await fetchWithAuth("https://discord.com/api/v9/users/@me/relationships", token);
  const result = {};

  for (const rel of relationships) {
    const friend = rel.user;

    // Fetch mutual friends (may not work if friend has blocked you)
    const mutualIds = await fetchWithAuth(
      `https://discord.com/api/v9/users/${friend.id}/relationships`,
      token
    ).then(res => res.map(u => u.id));

    result[friend.id] = {
      name: `${friend.username}#${friend.discriminator}`,
      global_name: friend.global_name || "",
      avatar: friend.avatar || "",
      mutual: mutualIds
    };

    console.log(`✅ Fetched: ${friend.username}`);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Avoid rate limits
  }

  // Save data as JSON file
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "friends_data.json"; // Universal export name
  a.click();
  URL.revokeObjectURL(url);

  console.log("📁 Exported as friends_data.json");
}

// Launch the function
getFriends(token);