import time
from data import clear

def print_menu():
    print("╔══════════════════════════════════════╗")
    print("║    📦  INVENTORY MANAGER             ║")
    print("╠══════════════════════════════════════╣")
    print("║  1.  Record Daily Inventory          ║")
    print("║  2.  View a Specific Day             ║")
    print("║  3.  Crunch the Averages             ║")
    print("║  4.  Get AI Business Insights        ║")
    print("║  5.  Exit                            ║")
    print("╚══════════════════════════════════════╝")


def main_menu():
    """Main hub that keeps the program running until the user quits."""
    while True:
        clear.clear_screen()
        print_menu()

        choice = input("\nWhat would you like to do? (1–5): ").strip()

        if choice == '1':
            from data import getdata
            getdata.run_getdata()
            input("\nPress Enter to return to the menu...")

        elif choice == '2':
            from data import report
            report.run_report()

        elif choice == '3':
            print("\nWarning: This will overwrite your previous average report.")
            confirm = input("Do you want to continue? (yes/no): ").strip().lower()
            if confirm in ('y', 'yes'):
                print("\nCrunching the numbers...")
                time.sleep(1)
                from data import average
                average.run_average()
                input("\nPress Enter to return to the menu...")
            else:
                print("Action cancelled.")
                time.sleep(1)

        elif choice == '4':
            from data import insight
            insight.generate_insights()
            input("\nPress Enter to return to the menu...")

        elif choice == '5':
            print("\nShutting down. Have a great day! 👋")
            time.sleep(1)
            break

        else:
            input("\nInvalid choice. Press Enter to try again...")


if __name__ == "__main__":
    main_menu()