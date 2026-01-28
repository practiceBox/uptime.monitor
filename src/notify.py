import os
import requests
from pathlib import Path


def send_discord_report(image_path: str):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return

    path = Path(image_path)
    if not path.exists():
        print("No image found to send.")
        return

    with open(path, "rb") as f:
        files = {
            "file": (path.name, f, "image/png")
        }
        data = {
            "content": "**Uptime Report & Performance**"
        }

        try:
            requests.post(webhook_url, files=files, data=data)
            print("Graph sent to Discord.")
        except Exception as e:
            print(f"Error sending message: {e}")


def send_discord_alert(url: str, error: str, site_name: str):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return
    data = {
        "content": f"**ALARM**: {site_name} ({url}) is OFFLINE! `{error}`"}
    requests.post(webhook_url, json=data)
    print(f"Alert sent to Discord for {site_name}.")
