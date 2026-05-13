import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()
print("╔══════════════════════════════════════╗")
print("║    LAUNCHER                          ║")
print("╠══════════════════════════════════════╣")
print("║  1. Start Terminal Menu              ║")
print("║  2. Start Web Server                 ║")
print("╚══════════════════════════════════════╝")

choice = input("\nWhich program do you want to run? (1 or 2): ").strip()

if choice == '1':
    import get
    get.main_menu()
elif choice == '2':
    import api
    print("\nStarting the web server on port 8000...")
    print("Keep this window open to keep the website live!")
    api.start_server()
else:
    print("Invalid choice. Closing launcher.")
    time.sleep(2)