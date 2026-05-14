import os
def clear_screen():
    """Clears the terminal for a clean menu experience."""
    os.system('cls' if os.name == 'nt' else 'clear')