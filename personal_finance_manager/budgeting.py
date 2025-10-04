from .database import get_db_connection

def set_budget(user_id: int):
    """Sets a monthly budget for a specific category."""
    try:
        category = input("Enter category to set budget for: ")
        amount = float(input("Enter budget amount: "))
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year (e.g., 2024): "))

        if not (1 <= month <= 12):
            print("Invalid month.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO budgets (user_id, category, amount, month, year) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, amount, month, year)
        )
        conn.commit()
        conn.close()
        print(f"Budget for '{category}' in {month}/{year} set to {amount:.2f}.")
    except ValueError:
        print("Invalid input. Please enter numbers for amount, month, and year.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_budgets(user_id: int):
    """Views all set budgets for the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, month, year FROM budgets WHERE user_id = ? ORDER BY year, month, category", (user_id,))
    budgets = cursor.fetchall()
    conn.close()

    if not budgets:
        print("No budgets set.")
        return

    print("\n--- Your Budgets ---")
    for b in budgets:
        print(f"Period: {b['month']}/{b['year']}, Category: {b['category']}, Amount: {b['amount']:.2f}")
    print("--------------------\n")

def check_budget_notification(user_id: int, category: str, month: int, year: int):
    """Checks if spending in a category has exceeded the budget and notifies the user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND category = ? AND month = ? AND year = ?",
        (user_id, category, month, year)
    )
    budget = cursor.fetchone()

    if not budget:
        conn.close()
        return  

    budget_amount = budget['amount']

    cursor.execute(
        "SELECT SUM(amount) as total_expenses FROM transactions WHERE user_id = ? AND type = 'expense' AND category = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?",
        (user_id, category, f"{month:02d}", str(year))
    )
    result = cursor.fetchone()
    total_expenses = result['total_expenses'] if result['total_expenses'] else 0
    conn.close()

    if total_expenses > budget_amount:
        print(f"\n--- BUDGET ALERT ---")
        print(f"You have exceeded your budget for '{category}' for {month}/{year}.")
        print(f"Budget: {budget_amount:.2f}, Spent: {total_expenses:.2f}, Over by: {total_expenses - budget_amount:.2f}")
        print("--------------------\n")