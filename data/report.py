import json
import os

DATA_DIR = "data/entries"


def load_inventory_data(week: int, day: int) -> dict | None:
    """Loads a specific daily record. Returns None if the file doesn't exist."""
    filepath = os.path.join(DATA_DIR, f"w{week}d{day}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)


def format_currency(value: float) -> str:
    """Formats a float as a signed currency string."""
    return f"+${value:.2f}" if value >= 0 else f"-${abs(value):.2f}"


def run_report():
    """Asks the user for a date and displays that day's sales in a clean table."""
    print("\n─── VIEW PAST REPORT ───────────────────")
    try:
        week = int(input("Which week? "))
        day = int(input("Which day (1–7)? "))
    except ValueError:
        print("❌ Please enter valid numbers.")
        input("Press Enter to return to the menu...")
        return

    data = load_inventory_data(week, day)

    if not data:
        print(f"\n❌ No records found for Week {week}, Day {day}.")
        input("Press Enter to return to the menu...")
        return

    print(f"\n{'═'*52}")
    print(f"  WEEK {data['week_number']}  |  DAY {data['day_number']}")
    print(f"{'═'*52}")
    print(f"  {'Product':<18} {'Made':>5} {'Sold':>5} {'Left':>5} {'Profit':>9}")
    print(f"  {'─'*18} {'─'*5} {'─'*5} {'─'*5} {'─'*9}")

    total_profit = 0.0
    for item in data['inventory']:
        name = item['name'].title()
        made = item['made']
        sold = item['sold']
        remaining = item.get('remaining', made - sold)
        profit = item.get('profit', 0.0)
        total_profit += profit
        print(f"  {name:<18} {made:>5} {sold:>5} {remaining:>5} {format_currency(profit):>9}")

    print(f"  {'─'*18} {'─'*5} {'─'*5} {'─'*5} {'─'*9}")
    print(f"  {'TOTAL':<35} {format_currency(total_profit):>9}")
    print(f"{'═'*52}")

    input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    run_report()
