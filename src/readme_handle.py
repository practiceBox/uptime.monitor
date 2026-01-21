import datetime
import re
from pathlib import Path
from typing import List, Dict


def update_readme(results: List[Dict]) -> bool:
    root_dir = Path(__file__).parent.parent
    readme_path = root_dir / "README.md"

    now = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = ["", "| WEBSITE | STATUS | INFO |", "| :--- | :---: | :--- |"]
    all_systems_go = True

    for entry in results:
        status_icon = "\u2714 OOOONNN" if entry['status'] else "\u274C OOOOFFF"
        lines.append(f"| {entry['url']} | {status_icon} | {entry['info']} |")
        if not entry['status']:
            all_systems_go = False

    lines.append(f"\n_Last Updated: {now}_")
    new_content = "\n".join(lines) + "\n"

    if not readme_path.exists():
        print("Error: README not found.")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    pattern = r"(<!-- START_STATUS -->)(.*?)(<!-- END_STATUS -->)"
    replacement = f"\\1{new_content}\\3"

    new_readme_content = re.sub(
        pattern, replacement, readme_content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme_content)

    print("README successfully updated.")
    return all_systems_go
