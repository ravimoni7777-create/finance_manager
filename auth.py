import getpass
import sqlite3
from .database import get_db_connection
from .utils import hash_password, verify_password

def register_user():
    """Handles user registration."""
    username = input("Enter a unique username: ")
    password = getpass.getpass("Enter a password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    conn = get_db_connection()
    try:
        password_hash = hash_password(password)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose another one.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def login_user():
    """Handles user login and returns user ID on success."""
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and verify_password(user['password_hash'], password):
            print("Login successful!")
            return user['id']
        else:
            print("Invalid username or password.")
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()