import requests

from typing import Tuple


def check_site(url: str, timeout: int = 5) -> Tuple[bool, str, float]:
    try:
        response = requests.get(url, timeout=timeout)
        latency = response.elapsed.total_seconds()
        if 200 <= response.status_code < 300:
            return True, str(response.status_code), latency
        else:
            return False, f"Status: {response.status_code}", 0.
    except requests.exceptions.Timeout:
        return False, "Timeout", 0.0
    except requests.exceptions.ConnectionError:
        return False, "DNS/Connection Error", 0.0
    except requests.exceptions.RequestException:
        return False, "Error", 0.0
