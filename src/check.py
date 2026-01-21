import requests
from typing import Tuple


def check_site(url: str, timeout: int = 5) -> Tuple[bool, str]:
    try:
        response = requests.get(url, timeout=timeout)
        if 200 <= response.status_code < 300:
            return True, str(response.status_code)
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "DNS/Connection Error"
    except requests.exceptions.RequestException:
        return False, "Error"
