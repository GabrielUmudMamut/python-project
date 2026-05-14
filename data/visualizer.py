import json
import os

DATA_DIR = "data/entries"
REPORT_FILE = os.path.join(DATA_DIR, "average_report.json")

BAR_WIDTH = 20  # Total character width of the progress bar


def load_averages() -> dict | None:
    """Loads the average report. Returns None if it doesn't exist yet."""
    if not os.path.exists(REPORT_FILE):
        print("❌ No average report found. Run the Average tool first.")
        return None
    with open(REPORT_FILE, "r") as f:
        return json.load(f)


def build_bar(sold: float, made: float) -> tuple[str, float]:
    """Returns a progress bar string and the sell-through percentage."""
    pct = (sold / made * 100) if made > 0 else 0.0
    filled = int(pct / (100 / BAR_WIDTH))
    bar = "█" * filled + "─" * (BAR_WIDTH - filled)
    return bar, pct


def draw_visuals():
    """Prints a text-based sell-through chart from the average report."""
    data = load_averages()
    if not data:
        return

    days = data["analysis_info"]["days_analyzed"]
    print(f"\n{'═'*56}")
    print(f"INVENTORY VISUALISER  |  Days analysed: {days}")
    print(f"{'═'*56}")
    print(f"  {'Product':<16} Sell-through")
    print(f"  {'─'*16} {'─'*34}")

    for item in data["averages"]:
        name = item["name"].title()[:15]
        bar, pct = build_bar(item["avg_sold"], item["avg_made"])

        # Colour-code the percentage: green ≥ 80 %, yellow ≥ 50 %, red otherwise
        if pct >= 80:
            pct_str = f"\033[92m{pct:5.1f}%\033[0m"
        elif pct >= 50:
            pct_str = f"\033[93m{pct:5.1f}%\033[0m"
        else:
            pct_str = f"\033[91m{pct:5.1f}%\033[0m"

        print(f"  {name:<16} [{bar}] {pct_str}")

    print(f"{'═'*56}\n")
