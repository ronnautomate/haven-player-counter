import os
import time
import requests

SERVER_IP = "haven.smpserver.net"
CHANNEL_ID = "1555444801694867476"

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

MC_API_URL = f"https://api.mcsrvstat.us/3/{SERVER_IP}"
DISCORD_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}"

HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

CHECK_INTERVAL = 300  # 5 minutes
last_channel_name = None

while True:
    try:
        response = requests.get(MC_API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        print("Minecraft API response:")
        print(data)

        if data.get("online"):
            players = data.get("players", {})
            online = players.get("online", 0)
            maximum = players.get("max", 0)

            print(f"API PLAYER COUNT: {online}/{maximum}")

            channel_name = f"{online}/{maximum} online"
        else:
            print("SERVER REPORTED OFFLINE")
            channel_name = "Offline"

        if channel_name != last_channel_name:
            response = requests.patch(
                DISCORD_URL,
                headers=HEADERS,
                json={"name": channel_name},
                timeout=15
            )

            if response.ok:
                print(f"Updated Discord: {channel_name}")
                last_channel_name = channel_name
            else:
                print(
                    f"Discord update failed: "
                    f"{response.status_code} {response.text}"
                )
        else:
            print(f"No change: {channel_name}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(CHECK_INTERVAL)
