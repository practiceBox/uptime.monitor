import datetime
import re
from pathlib import Path
from typing import List, Dict


def update_readme(results: List[Dict]) -> bool:
    root_dir = Path(__file__).parent.parent
    readme_path = root_dir / "README.md"

    now = datetime.datetime.now(
        datetime.timezone.utc).strftime("%d.%m.%Y %H:%M UTC")

    md_content = [
        "",
        "![Uptime Graph](uptime_chart.png)",
        "",
        "| Website | Status | Latency | Info |",
        "| :--- | :---: | :---: | :--- |"
    ]

    all_systems_go = True

    for entry in results:
        is_online = entry['status']
        latency = f"{entry['latency']:.2f}s"
        name = entry['name']
        info = entry['info']

        if is_online:
            color = "success"
            status_text = "ONLINE"
        else:
            color = "critical"
            status_text = "OFFLINE"
            all_systems_go = False

        badge = f"![Status](https://img.shields.io/badge/Status-{status_text}-{color}?style=flat-square)"

        md_content.append(f"| **{name}** | {badge} | `{latency}` | {info} |")

    md_content.append(f"\n_Last updated: {now}_")
    new_block = "\n".join(md_content) + "\n"

    if not readme_path.exists():
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    pattern = r"(<!-- START_STATUS -->)(.*?)(<!-- END_STATUS -->)"
    replacement = f"\\1{new_block}\\3"

    new_readme_content = re.sub(
        pattern, replacement, readme_content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme_content)

    return all_systems_go
