from .database import get_db_connection

def generate_financial_report(user_id: int):
    """Generates a monthly or yearly financial report."""
    report_type = input("Generate report for (month/year): ").lower()

    try:
        if report_type == 'month':
            year = int(input("Enter year (e.g., 2024): "))
            month = int(input("Enter month (1-12): "))
            if not (1 <= month <= 12):
                print("Invalid month.")
                return
            _generate_monthly_report(user_id, year, month)
        elif report_type == 'year':
            year = int(input("Enter year (e.g., 2024): "))
            _generate_yearly_report(user_id, year)
        else:
            print("Invalid report type.")
    except ValueError:
        print("Invalid input for year or month.")

def _generate_monthly_report(user_id: int, year: int, month: int):
    """Generates and prints a financial report for a specific month."""
    conn = get_db_connection()
    cursor = conn.cursor()
    month_str = f"{month:02d}"

    # Total Income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, str(year), month_str))
    total_income = cursor.fetchone()[0] or 0.0

    # Total Expenses
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, str(year), month_str))
    total_expenses = cursor.fetchone()[0] or 0.0

    # Expenses by Category
    cursor.execute("SELECT category, SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ? GROUP BY category", (user_id, str(year), month_str))
    expenses_by_category = cursor.fetchall()
    conn.close()

    savings = total_income - total_expenses

    print(f"\n--- Monthly Report for {month}/{year} ---")
    print(f"Total Income:   {total_income:10.2f}")
    print(f"Total Expenses: {total_expenses:10.2f}")
    print(f"Net Savings:    {savings:10.2f}")
    print("\n--- Expenses by Category ---")
    if expenses_by_category:
        for item in expenses_by_category:
            print(f"- {item['category']:<20}: {item['total']:>10.2f}")
    else:
        print("No expenses recorded for this month.")
    print("----------------------------------\n")

def _generate_yearly_report(user_id: int, year: int):
    """Generates and prints a financial report for a specific year."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total Income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ?", (user_id, str(year)))
    total_income = cursor.fetchone()[0] or 0.0

    # Total Expenses
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ?", (user_id, str(year)))
    total_expenses = cursor.fetchone()[0] or 0.0

    # Expenses by Category
    cursor.execute("SELECT category, SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ? GROUP BY category", (user_id, str(year)))
    expenses_by_category = cursor.fetchall()
    conn.close()

    savings = total_income - total_expenses

    print(f"\n--- Yearly Report for {year} ---")
    print(f"Total Income:   {total_income:10.2f}")
    print(f"Total Expenses: {total_expenses:10.2f}")
    print(f"Net Savings:    {savings:10.2f}")
    print("\n--- Expenses by Category ---")
    if expenses_by_category:
        for item in expenses_by_category:
            print(f"- {item['category']:<20}: {item['total']:>10.2f}")
    else:
        print("No expenses recorded for this year.")
    print("------------------------------\n")