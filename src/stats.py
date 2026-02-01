import json

from pathlib import Path

HISTORY_FILE = Path('data/history.json')

def get_uptime_percentage(site_name: str ) -> float:
    if not HISTORY_FILE.exists():
        return 100.0
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
            history = json.load(file)
    except (json.JSONDecodeError, OSError):
        return 100.0
    
    if not history:
        return 100.0
    
    total_checks = 0
    up_checks = 0


    for entry in history:
        if site_name in entry:
            total_checks += 1
            if entry[site_name] > 0:
                up_checks += 1

    if total_checks == 0:
        return 100.0
    
    return (up_checks / total_checks) * 100
