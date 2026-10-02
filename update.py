import os
import requests

SERVER_IP = "haven.smpserver.net"
CHANNEL_ID = "1555444801694867476"

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Check Minecraft server
url = f"https://api.mcsrvstat.us/3/{SERVER_IP}"

response = requests.get(url, timeout=15)
response.raise_for_status()

data = response.json()

if data.get("online"):
    players = data.get("players", {})
    online = players.get("online", 0)
    maximum = players.get("max", 0)

    channel_name = f"{online}/{maximum} online"
else:
    channel_name = "Offline"

# Update Discord channel
discord_url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}"

headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.patch(
    discord_url,
    headers=headers,
    json={"name": channel_name},
    timeout=15
)

response.raise_for_status()

print(f"Updated Discord channel to: {channel_name}")
