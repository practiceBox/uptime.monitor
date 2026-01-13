import sys

import requests


def check_site(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            print(f"{url} is ONLINE")
            return True
        else:
            print(f"{url} status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{url} is OFFLINE. Error: {e}")
        return False


if __name__ == "__main__":
    sites = [
        "https://www.ademoencue.de",
        "https://adminhype.github.io/joinKanban/",
        "https://kanmind.ademoencue.de/",
        "https://coderr.ademoencue.de/"
    ]
    all_up = True

    for site in sites:
        if not check_site(site):
            all_up = False

    if not all_up:
        sys.exit(1)
