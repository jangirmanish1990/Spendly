import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "spendly.db"


def get_db():
    """
    Opens connection to SQLite database.
    Sets row_factory for dictionary-like access and enables foreign keys.
    Returns the connection.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Creates users and expenses tables if they don't exist.
    Safe to call multiple times.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """
    Inserts demo user and sample expenses.
    Safe to call multiple times - checks for existing data before inserting.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    demo_password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password_hash)
    )

    # Get the demo user's id
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",))
    demo_user_id = cursor.fetchone()[0]

    # Insert 8 sample expenses across different categories
    sample_expenses = [
        (50.00, "Food", "2026-04-01", "Lunch at restaurant"),
        (25.50, "Transport", "2026-04-02", "Uber ride"),
        (120.00, "Bills", "2026-04-03", "Electric bill"),
        (45.00, "Health", "2026-04-05", "Pharmacy"),
        (35.00, "Entertainment", "2026-04-07", "Movie tickets"),
        (89.99, "Shopping", "2026-04-08", "Clothing"),
        (15.00, "Other", "2026-04-09", "Miscellaneous"),
        (65.00, "Food", "2026-04-10", "Grocery shopping"),
    ]

    for amount, category, date, description in sample_expenses:
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (demo_user_id, amount, category, date, description)
        )

    conn.commit()
    conn.close()
