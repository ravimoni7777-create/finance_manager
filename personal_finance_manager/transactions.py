from .database import get_db_connection
from datetime import datetime
from . import budgeting

def add_transaction(user_id: int):
    """Adds a new transaction for the user."""
    try:
        trans_type = input("Enter transaction type (income/expense): ").lower()
        if trans_type not in ['income', 'expense']:
            print("Invalid transaction type.")
            return

        amount = float(input("Enter amount: "))
        category = input("Enter category (e.g., Food, Salary): ")
        description = input("Enter description (optional): ")
        date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ")

        date = date_str if date_str else datetime.now().strftime('%Y-%m-%d')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, category, description, date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, trans_type, amount, category, description, date)
        )
        conn.commit()
        print("Transaction added successfully.")
        conn.close()

        if trans_type == 'expense':
            trans_date = datetime.strptime(date, '%Y-%m-%d')
            budgeting.check_budget_notification(user_id, category, trans_date.month, trans_date.year)

    except ValueError:
        print("Invalid amount. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_transactions(user_id: int):
    """Displays all transactions for the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, type, category, amount, description FROM transactions WHERE user_id = ? ORDER BY date DESC", (user_id,))
    transactions = cursor.fetchall()
    conn.close()

    if not transactions:
        print("No transactions found.")
        return

    print("\n--- Your Transactions ---")
    print(f"{'ID':<5}{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':<10}{'Description'}")
    print("-" * 70)
    for t in transactions:
        print(f"{t['id']:<5}{t['date']:<12}{t['type'].capitalize():<10}{t['category']:<15}{t['amount']:.2f}{' ':<5}{t['description']}")
    print("-" * 70)

def update_transaction(user_id: int):
    """Updates an existing transaction."""
    view_transactions(user_id)
    try:
        trans_id = int(input("Enter the ID of the transaction to update: "))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM transactions WHERE id = ? AND user_id = ?", (trans_id, user_id))
        if not cursor.fetchone():
            print("Transaction ID not found or you don't have permission to edit it.")
            conn.close()
            return

        print("Enter new details (leave blank to keep current value):")

        updates = []
        params = []

        new_amount_str = input("New amount: ")
        if new_amount_str:
            updates.append("amount = ?")
            params.append(float(new_amount_str))

        new_category = input("New category: ")
        if new_category:
            updates.append("category = ?")
            params.append(new_category)

        new_description = input("New description: ")
        if new_description:
            updates.append("description = ?")
            params.append(new_description)

        if not updates:
            print("No changes to apply.")
            return

        params.append(trans_id)
        query = f"UPDATE transactions SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()
        print("Transaction updated successfully.")

    except ValueError:
        print("Invalid ID or amount.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_transaction(user_id: int):
    """Deletes a transaction."""
    view_transactions(user_id)
    try:
        trans_id = int(input("Enter the ID of the transaction to delete: "))
        confirm = input(f"Are you sure you want to delete transaction {trans_id}? (y/n): ").lower()
        if confirm == 'y':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (trans_id, user_id))
            conn.commit()
            if cursor.rowcount > 0:
                print("Transaction deleted successfully.")
            else:
                print("Transaction ID not found or you don't have permission to delete it.")
            conn.close()
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Invalid ID.")
    except Exception as e:
        print(f"An error occurred: {e}")