import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from src.readme_handle import update_readme
from src.notify import send_discord_alert
from src.check import check_site

load_dotenv()


def load_config():
    config_path = Path("config/sites.json")
    if not config_path.exists():
        print("Config file config/sites.json missing!")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    sites = load_config()
    results = []

    print(f"Starting check for {len(sites)} sites..")

    for site in sites:
        url = site["url"]
        name = site.get("name", url)

        is_online, info = check_site(url)
        print(
            f"Checked {name}: {'Online' if is_online else 'Offline'} ({info})")

        if not is_online:
            send_discord_alert(url, info, name)

        results.append({
            "url": url,
            "status": is_online,
            "info": info
        })

    all_good = update_readme(results)

    if not all_good:
        print("At least one system is offline.")
        sys.exit(1)
    else:
        print("All systems online.")
        sys.exit(0)


if __name__ == "__main__":
    main()
