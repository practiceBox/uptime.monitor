import datetime
import re
from pathlib import Path
from typing import List, Dict

from src.stats import get_uptime_percentage


def update_readme(results: List[Dict]) -> bool:
    root_dir = Path(__file__).parent.parent
    readme_path = root_dir / "README.md"

    now = datetime.datetime.now(
        datetime.timezone.utc).strftime("%d.%m.%Y %H:%M UTC")

    md_content = [
        "",
        "![Uptime Graph](uptime_chart.png)",
        "",
        "| Website | Status | Latency | Info | Uptime |",
        "| :--- | :---: | :---: | :--- | :---: |"
    ]

    all_systems_go = True

    for entry in results:
        is_online = entry["status"]
        latency = f"{entry['latency']:.2f}s"
        name = entry["name"]
        info = entry["info"]

        uptime_pct = get_uptime_percentage(name)
        uptime_str = f"{uptime_pct:.1f}%25"

        if uptime_pct >= 99.0:
            uptime_color = "brightgreen"
        elif uptime_pct >= 95.0:
            uptime_color = "green"
        elif uptime_pct >= 90.0:
            uptime_color = "yellow"
        else:
            uptime_color = "red"
        
        uptime_badge = f"![Uptime](https://img.shields.io/static/v1?label=Uptime&message={uptime_str}&color={uptime_color}&style=flat-square)"

        if is_online:
            color = "success"
            status_text = "ONLINE"
        else:
            color = "critical"
            status_text = "OFFLINE"
            all_systems_go = False

        status_badge = f"![Status](https://img.shields.io/badge/Status-{status_text}-{color}?style=flat-square)"

        md_content.append(f"| **{name}** | {status_badge} | `{latency}` | {info} | {uptime_badge} |")

    md_content.append(f"\n_Last updated: {now}_")
    new_block = "\n".join(md_content) + "\n"

    if not readme_path.exists():
        return False

    with open(readme_path, "r", encoding="utf-8") as file_path:
        readme_content = file_path.read()

    pattern = r"(<!-- START_STATUS -->)(.*?)(<!-- END_STATUS -->)"
    replacement = f"\\1{new_block}\\3"

    new_readme_content = re.sub(
        pattern, replacement, readme_content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as file_path:
        file_path.write(new_readme_content)

    return all_systems_go
