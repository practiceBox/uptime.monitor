import os
import requests


def send_discord_alert(url: str, error: str, site_name: str):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return

    content = f"**ALARM**: {site_name} ({url}) is offline: `{error}`"

    data = {
        "content": content,
        "username": "Uptime Monitor"
    }

    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
