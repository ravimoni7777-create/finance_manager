import shutil
from . import auth
from . import transactions
from . import reports
from . import budgeting
from .database import create_tables, DB_FILE

def logged_in_menu(user_id: int):
    """Displays the menu for a logged-in user."""
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Generate Financial Report")
        print("6. Set Budget")
        print("7. View Budgets")
        print("8. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            transactions.add_transaction(user_id)
        elif choice == '2':
            transactions.view_transactions(user_id)
        elif choice == '3':
            transactions.update_transaction(user_id)
        elif choice == '4':
            transactions.delete_transaction(user_id)
        elif choice == '5':
            reports.generate_financial_report(user_id)
        elif choice == '6':
            budgeting.set_budget(user_id)
        elif choice == '7':
            budgeting.view_budgets(user_id)
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    """Displays the main menu for the application."""
    create_tables()
    while True:
        print("\n--- Personal Finance Manager ---")
        print("1. Register")
        print("2. Login")
        print("3. Backup Data")
        print("4. Restore Data")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            auth.register_user()
        elif choice == '2':
            user_id = auth.login_user()
            if user_id:
                logged_in_menu(user_id)
        elif choice == '3':
            _backup_data()
        elif choice == '4':
            _restore_data()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def _backup_data():
    """Backs up the database file."""
    backup_file = input("Enter backup file path (e.g., backup.db): ")
    try:
        shutil.copy(DB_FILE, backup_file)
        print(f"Data successfully backed up to {backup_file}")
    except FileNotFoundError:
        print(f"Error: Database file '{DB_FILE}' not found. Nothing to back up.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

def _restore_data():
    """Restores the database from a backup file."""
    backup_file = input("Enter backup file path to restore from: ")
    confirm = input(f"This will OVERWRITE current data. Are you sure? (y/n): ").lower()
    if confirm == 'y':
        try:
            shutil.copy(backup_file, DB_FILE)
            print("Data successfully restored.")
        except FileNotFoundError:
            print(f"Error: Backup file '{backup_file}' not found.")
        except Exception as e:
            print(f"An error occurred during restore: {e}")
    else:
        print("Restore cancelled.")

if __name__ == "__main__":
    main_menu()