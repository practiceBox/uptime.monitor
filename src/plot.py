import json
import datetime
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict

HISTORY_FILE = Path("data/history.json")
MAX_HISTORY_ENTRIES = 30

CHART_THEME = {
    'style': 'dark_background',
    'colors': ['#034732', '#FFE66D', '#ffff00', '#3F6C51', '#DD1C1A'],
    'title': "Latency",
    'xlabel': "Time (UTC)",
    'ylabel': "Seconds",
    'threshold_line': 10.0,
    'threshold_color': 'red',
    'grid_alpha': 1,
    'fill_alpha': 0.5,
    'line_width': 5
}


def save_history(results: List[Dict]) -> List[Dict]:
    history = []

    if not HISTORY_FILE.parent.exists():
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    timestamp = datetime.datetime.now().strftime("%H:%M")

    snapshot = {"time": timestamp}
    for entry in results:
        latency = entry['latency'] if entry['status'] else 0
        snapshot[entry['name']] = latency

    history.append(snapshot)

    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return history


def _apply_chart_style(ax: List[str]):
    theme = CHART_THEME

    ax.axhline(y=theme['threshold_line'], color=theme['threshold_color'],
               linestyle='--', alpha=0.5, linewidth=1, label="Slow Threshold")

    ax.set_title(theme['title'], fontsize=26,
                 fontweight='bold', color='white', pad=20)
    ax.set_ylabel(theme['ylabel'], fontsize=14)
    ax.set_xlabel(theme['xlabel'], fontsize=14)

    ax.grid(True, linestyle=':', alpha=theme['grid_alpha'])
    ax.legend(loc='upper left', fontsize='small',
              frameon=True, facecolor='#222')

    plt.xticks(rotation=45)


def create_graph(history: List[Dict], output_file="uptime_chart.png") -> str:
    if not history:
        return None

    plt.style.use(CHART_THEME['style'])  # style global

    timestamps = [h["time"] for h in history]
    site_names = [key for key in history[-1].keys() if key != "time"]

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = CHART_THEME['colors']

    for i, site in enumerate(site_names):
        latencies = [entry.get(site, 0) for entry in history]

        color = colors[i % len(colors)]

        ax.plot(timestamps, latencies, marker='.', linestyle='-',
                linewidth=CHART_THEME['line_width'], label=site, color=color)

        ax.fill_between(timestamps, latencies,
                        alpha=CHART_THEME['fill_alpha'], color=color)

    _apply_chart_style(ax)

    plt.tight_layout()
    plt.savefig(output_file, dpi=100, facecolor=fig.get_facecolor())
    plt.close()

    return output_file
