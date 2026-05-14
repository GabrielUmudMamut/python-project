import json
import os
import data.visualizer as visualizer

DATA_DIR = "data/entries"
OUTPUT_FILE = os.path.join(DATA_DIR, "average_report.json")


def load_data(week: int, day: int) -> dict | None:
    """Loads a daily record if it exists, otherwise returns None."""
    filepath = os.path.join(DATA_DIR, f"w{week}d{day}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None


def get_valid_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def run_average():
    """Loops through a range of days and calculates per-item averages."""
    print("\n─── AVERAGE CALCULATOR ─────────────────")
    try:
        start_week = get_valid_int("Starting week number: ")
        start_day = get_valid_int("Starting day (1-7): ")
        num_days = get_valid_int("How many consecutive days to analyse? ")
    except KeyboardInterrupt:
        print("\nCancelled.")
        return

    if not (1 <= start_day <= 7):
        print("Day must be between 1 and 7.")
        return

    # Accumulate stats across the date range
    stats: dict[str, dict] = {}
    days_found = 0
    current_week, current_day = start_week, start_day

    for _ in range(num_days):
        data = load_data(current_week, current_day)

        if data:
            days_found += 1
            for item in data["inventory"]:
                name = item["name"].lower().strip()
                cost = item.get("cost", 0.0)
                price = item.get("price", 0.0)

                if name not in stats:
                    stats[name] = {
                        "made": 0, "sold": 0, "remaining": 0,
                        "total_cost": 0.0, "total_revenue": 0.0,
                        "total_waste_loss": 0.0, "count": 0,
                    }

                s = stats[name]
                s["made"] += item["made"]
                s["sold"] += item["sold"]
                s["remaining"] += item["remaining"]
                s["total_cost"] += item["made"] * cost
                s["total_revenue"] += item["sold"] * price
                s["total_waste_loss"] += item["remaining"] * cost
                s["count"] += 1

        # Advance date, rolling over the week boundary
        current_day += 1
        if current_day > 7:
            current_day = 1
            current_week += 1

    if days_found == 0:
        print("No data files found for that date range.")
        return

    # Build the final averaged report
    averages = []
    for name, s in stats.items():
        count = s["count"]
        avg_revenue = s["total_revenue"] / count
        avg_cost = s["total_cost"] / count

        averages.append({
            "name": name.title(),
            "avg_made": round(s["made"] / count, 2),
            "avg_sold": round(s["sold"] / count, 2),
            "avg_remaining": round(s["remaining"] / count, 2),
            "avg_profit": round(avg_revenue - avg_cost, 2),
            "avg_loss": round(s["total_waste_loss"] / count, 2),
        })

    report = {
        "analysis_info": {
            "days_analyzed": days_found,
            "start_point": f"w{start_week}d{start_day}",
        },
        "averages": averages,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print(f"\n✅ Report saved to {OUTPUT_FILE} ({days_found} day(s) analysed).")
    visualizer.draw_visuals()
