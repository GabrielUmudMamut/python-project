import json
import os

DATA_DIR = "data/entries"
PRICES_FILE = os.path.join(DATA_DIR, "prices.json")
MANIFEST_FILE = os.path.join(DATA_DIR, "manifest.json")


def clear_screen():
    """Clears the terminal so the dashboard always looks fresh."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_int(prompt):
    """Keeps asking until the user provides a valid whole number."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def get_valid_float(prompt):
    """Keeps asking until the user provides a valid decimal number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number (decimals are fine).")


def load_prices():
    """Loads the saved price memory bank, returning an empty dict if missing."""
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r") as f:
            return json.load(f)
    return {}


def save_prices(prices: dict):
    """Saves the updated prices back to the memory bank."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PRICES_FILE, "w") as f:
        json.dump(prices, f, indent=4)


def load_manifest() -> dict:
    """Loads the file manifest, returning a blank one if missing or corrupt."""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {"files_available": []}


def save_manifest(manifest: dict):
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=4)


def collect_item_data(item_num: int, saved_prices: dict) -> dict:
    """Collects all data for a single inventory item and returns it as a dict."""
    name = input(f"\n  Product #{item_num} name: ").lower().strip()
    display_name = name.title()

    # --- Price memory logic ---
    if name in saved_prices:
        old = saved_prices[name]
        print(f"  💾 Saved: Cost = ${old['cost']:.2f} | Sell = ${old['price']:.2f}")
        change = input(f"  Use saved prices for {display_name}? (y/n): ").strip().lower()

        if change in ('n', 'no'):
            cost = get_valid_float(f"  New cost per {display_name} (e.g. 0.50): $")
            price = get_valid_float(f"  New sell price per {display_name} (e.g. 2.50): $")
            saved_prices[name] = {"cost": cost, "price": price}
        else:
            cost, price = old["cost"], old["price"]
    else:
        cost = get_valid_float(f"  Cost to make one {display_name} (e.g. 0.50): $")
        price = get_valid_float(f"  Selling price for one {display_name} (e.g. 2.50): $")
        saved_prices[name] = {"cost": cost, "price": price}

    made = get_valid_int(f"  How many {display_name}s did you stock? ")

    while True:
        sold = get_valid_int(f"  How many {display_name}s did you sell? ")
        if sold <= made:
            break
        print(f"Can't sell more than you made ({made}). Try again.")

    remaining = made - sold
    revenue = sold * price
    total_cost = made * cost
    profit = revenue - total_cost

    return {
        "name": name,
        "cost": cost,
        "price": price,
        "made": made,
        "sold": sold,
        "remaining": remaining,
        "profit": round(profit, 2),
    }


def run_getdata():
    clear_screen()
    print("\n─── NEW DAILY RECORD ───────────────────")

    week_num = get_valid_int("Week number: ")
    day_num = get_valid_int("Day number (1 = Mon, 7 = Sun): ")

    while not (1 <= day_num <= 7):
        print("Day must be between 1 and 7.")
        day_num = get_valid_int("Day number (1–7): ")

    total_products = get_valid_int("How many different product types today? ")

    daily_record = {
        "week_number": week_num,
        "day_number": day_num,
        "total_item_types": total_products,
        "inventory": [],
    }

    saved_prices = load_prices()

    print("\n─── ITEM DETAILS ───────────────────────")
    for i in range(1, total_products + 1):
        item = collect_item_data(i, saved_prices)
        daily_record["inventory"].append(item)

    # Persist price memory
    save_prices(saved_prices)

    # Save the daily record
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"w{week_num}d{day_num}.json"
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(daily_record, f, indent=4)

    # Update manifest
    manifest = load_manifest()
    if filename not in manifest["files_available"]:
        manifest["files_available"].append(filename)
    save_manifest(manifest)

    print(f"\nSaved to {filepath}. Price memory updated.")
