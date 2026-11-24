
import os
import time
import requests
from mcstatus import JavaServer

SERVER_ADDRESS = "haven.smpserver.net"
CHANNEL_ID = "1555444801694867476"

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

DISCORD_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}"

HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

CHECK_INTERVAL = 15
RUN_FOR_SECONDS = 240

server = JavaServer.lookup(SERVER_ADDRESS)

last_channel_name = None
deadline = time.monotonic() + RUN_FOR_SECONDS

print("Haven Player Counter started")

while time.monotonic() < deadline:
    try:
        status = server.status()

        online = status.players.online
        maximum = status.players.max

        channel_name = f"{online}/{maximum} online"

        print(f"Minecraft players: {channel_name}")

        if channel_name != last_channel_name:
            response = requests.patch(
                DISCORD_URL,
                headers=HEADERS,
                json={"name": channel_name},
                timeout=10
            )

            response.raise_for_status()

            last_channel_name = channel_name
            print(f"Discord updated: {channel_name}")
        else:
            print("No change needed")

    except Exception as error:
        print(f"Update error: {error}")

    remaining = deadline - time.monotonic()

    if remaining > 0:
        time.sleep(min(CHECK_INTERVAL, remaining))

print("Player counter finished successfully")
