import json
import os

DATA_DIR = "data/entries"
MANIFEST_FILE = os.path.join(DATA_DIR, "manifest.json")


def test_manifest():
    """Loads and pretty-prints the manifest file to verify its contents."""
    if not os.path.exists(MANIFEST_FILE):
        print(f"Manifest not found at '{MANIFEST_FILE}'.")
        print("Run 'Record Daily Inventory' first to create it.")
        return

    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Manifest loaded successfully:")
        print(json.dumps(data, indent=4))
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from '{MANIFEST_FILE}'. The file may be corrupt.")


if __name__ == "__main__":
    test_manifest()
