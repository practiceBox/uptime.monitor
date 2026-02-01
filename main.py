import json
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.readme_handle import update_readme
from src.check import check_site
from src.plot import save_history, create_graph
from src.notify import send_discord_report, send_discord_alert

load_dotenv()


def load_config():
    config_path = Path("config/sites.json")
    if not config_path.exists():
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as file_path:
        return json.load(file_path)


def main():
    sites = load_config()
    results = []

    print(f"Check {len(sites)} Sites...")

    for site in sites:
        url = site["url"]
        name = site.get("name", url)

        is_online, info, latency = check_site(url)

        display_info = f"{info}"
        if is_online:
            display_info += f" ({latency:.2f}s)"

        print(f"{name}: {display_info}")

        if not is_online:
            send_discord_alert(url, info, name)

        results.append({
            "url": url,
            "name": name,
            "status": is_online,
            "info": display_info,
            "latency": latency
        })

    print("save History...")
    history = save_history(results)
    
    print("Create Graph...")
    image_path = create_graph(history)

    print("update README...")
    all_good = update_readme(results)

    if image_path:
        send_discord_report(image_path)

    if not all_good:
        sys.exit(1)


if __name__ == "__main__":
    main()
