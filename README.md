# Personal Finance Management Application

A command-line application to help users manage their personal finances by tracking income, expenses, and generating financial reports.

## Features

- **User Management**: Secure user registration and login.
- **Transaction Tracking**: Add, view, update, and delete income and expense records.
- **Categorization**: Assign categories to transactions (e.g., Food, Rent, Salary).
- **Budgeting**: Set monthly budgets for different expense categories and receive alerts when you exceed them.
- **Reporting**: Generate monthly and yearly financial summaries, including total income, expenses, and savings.
- **Data Persistence**: All data is stored locally in a SQLite database.
- **Backup & Restore**: Simple file-based backup and restore functionality for your financial data.

## Project Structure

```
personal_finance_manager/
├── main.py                 # Main entry point of the application
├── auth.py                 # User registration and authentication
├── transactions.py         # Income and expense tracking
├── reports.py              # Financial report generation
├── budgeting.py            # Budgeting features
├── database.py             # Database interaction (SQLite)
├── utils.py                # Utility functions (e.g., password hashing)
├── data/
│   └── finance.db          # SQLite database file (created on first run)
└── README.md               # This file
```

## Installation

1.  **Clone the repository or download the files.**

2.  **Navigate to the project directory.**

3.  This project uses only Python's standard libraries, so no external packages are required to be installed.

## Usage

1.  **Run the application:**

    To run the application, execute the `main.py` file as a module from the parent directory of `personal_finance_manager`.

    ```bash
    python -m personal_finance_manager.main
    ```

2.  **Follow the on-screen prompts:**
    -   The first time you run the application, a `data` directory and a `finance.db` database file will be created automatically.
    -   You can **Register** a new user account or **Login** if you already have one.
    -   Once logged in, you will have access to the main menu to manage your finances.

### Main Menu Options

-   **Add/View/Update/Delete Transaction**: Manage your income and expense records.
-   **Generate Financial Report**: Create a summary for a specific month or year.
-   **Set/View Budget**: Define and see spending limits for categories.
-   **Logout**: Return to the main login/register screen.

### Data Backup and Restore

From the initial screen (before logging in), you can **Backup** your data to a file or **Restore** it from a previous backup. Use the restore function with caution as it will overwrite all current data.