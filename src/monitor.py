import sys
import requests
import datetime
from pathlib import Path
from typing import List, Tuple


def check_site(url: str) -> Tuple[bool, str]:
    try:
        response = requests.get(url, timeout=5)

        if 200 <= response.status_code < 300:
            return True, str(response.status_code)
        else:
            return False, str(response.status_code)

    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "DNS/Connection Error"
    except requests.exceptions.RequestException:
        return False, "Error"


def update_readme(results: List[Tuple[str, bool, str]]) -> bool:
    readme_path = (Path(__file__).parent.parent / "README.md").resolve()
    now = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    markdown_lines = [
        "",
        "| Webseite | Status | Info |",
        "| :--- | :---: | :--- |"
    ]
    all_systems_go = True

    for url, is_online, info in results:
        status_icon = "\u2714 Online" if is_online else "\u2718 Offline"

        markdown_lines.append(f"| {url} | {status_icon} | {info} |")

        if not is_online:
            all_systems_go = False

    markdown_lines.append(f"\n_Zuletzt aktualisiert: {now}_")
    new_table_content = "\n".join(markdown_lines) + "\n"

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: README not found at {readme_path}")
        return False

    start_marker = "<!-- START_STATUS -->"
    end_marker = "<!-- END_STATUS -->"

    if start_marker in content and end_marker in content:
        parts = content.split(start_marker)
        before_part = parts[0]

        rest = parts[1].split(end_marker)
        after_part = rest[1]

        new_readme = f"{before_part}{start_marker}{new_table_content}{end_marker}{after_part}"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("README updated successfully.")
    else:
        print("Markers <!-- START_STATUS --> and <!-- END_STATUS --> not found!")

    return all_systems_go


if __name__ == "__main__":
    sites = [
        "https://www.ademoencue.de",
        "https://adminhype.github.io/joinKanban/",
        "https://kanmind.ademoencue.de/",
        "https://coderr.ademoencue.de/"
    ]
    collected_results = []

    print("Checking sites...")
    for site in sites:
        success, info = check_site(site)
        print(f"Checked {site}: {success} ({info})")
        collected_results.append((site, success, info))

    all_good = update_readme(collected_results)

    if not all_good:
        print("Some systems are offline.")
        sys.exit(1)
