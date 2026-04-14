import sqlite3
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Parse arguments
user_id = 2
count = 5
months = 3

# Category definitions with realistic Indian descriptions and amounts (INR)
CATEGORIES = {
    "Food": {"min": 50, "max": 800, "weight": 30, "descriptions": [
        "Lunch at local restaurant", "Grocery shopping", "Street food",
        "Dinner with friends", "Morning breakfast", "Weekend special meal"
    ]},
    "Transport": {"min": 20, "max": 500, "weight": 20, "descriptions": [
        "Auto rickshaw fare", "Uber/Ola ride", "Metro card recharge",
        "Bus pass", "Fuel for scooter", "Taxi to airport"
    ]},
    "Bills": {"min": 200, "max": 3000, "weight": 20, "descriptions": [
        "Electricity bill", "Mobile recharge", "Internet bill",
        "Water bill", "Gas cylinder", "DTH subscription"
    ]},
    "Health": {"min": 100, "max": 2000, "weight": 10, "descriptions": [
        "Pharmacy medicines", "Doctor consultation", "Health checkup",
        "Gym membership", "Yoga class fee", "Medical test"
    ]},
    "Entertainment": {"min": 100, "max": 1500, "weight": 10, "descriptions": [
        "Movie tickets", "Netflix subscription", "Concert entry",
        "Gaming subscription", "Book purchase", "Weekend outing"
    ]},
    "Shopping": {"min": 200, "max": 5000, "weight": 7, "descriptions": [
        "New clothes", "Electronics accessory", "Home decor item",
        "Gift for friend", "Kitchen appliance", "Personal care items"
    ]},
    "Other": {"min": 50, "max": 1000, "weight": 3, "descriptions": [
        "Miscellaneous purchase", "Donation", "Stationery",
        "Pet supplies", "Household item", "Small repair"
    ]}
}

def get_db_connection():
    """Use the same connection pattern as db.py"""
    from database.db import get_db
    return get_db()

def generate_expenses(user_id, count, months):
    """Generate expenses spread across the specified months"""
    expenses = []
    today = datetime.now()

    # Create a list of categories with weights for proportional distribution
    weighted_categories = []
    for cat, data in CATEGORIES.items():
        weighted_categories.extend([cat] * data["weight"])

    # Generate random dates across the past 'months' months
    for _ in range(count):
        # Random date within the past 'months' months
        random_days = random.randint(0, months * 30)
        expense_date = today - timedelta(days=random_days)
        date_str = expense_date.strftime("%Y-%m-%d")

        # Select category based on weights
        category = random.choice(weighted_categories)
        cat_data = CATEGORIES[category]

        # Generate random amount within range
        amount = round(random.uniform(cat_data["min"], cat_data["max"]), 2)

        # Select random description
        description = random.choice(cat_data["descriptions"])

        expenses.append((user_id, amount, category, date_str, description))

    return expenses

def insert_expenses(expenses):
    """Insert all expenses in a single transaction"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Begin transaction (implicit in sqlite3, but being explicit)
        cursor.execute("BEGIN")

        for expense in expenses:
            cursor.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                expense
            )

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        return False
    finally:
        conn.close()

def main():
    # Generate expenses
    expenses = generate_expenses(user_id, count, months)

    # Insert expenses
    if insert_expenses(expenses):
        # Fetch inserted expenses for confirmation
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, amount, category, date, description FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )
        all_expenses = cursor.fetchall()

        # Get date range
        cursor.execute(
            "SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?",
            (user_id,)
        )
        min_date, max_date = cursor.fetchone()

        conn.close()

        print(f"Successfully inserted {count} expenses for user {user_id}")
        print(f"Date range: {min_date} to {max_date}")
        print("\nSample of 5 inserted records:")
        print("-" * 80)
        for exp in all_expenses[:5]:
            print(f"ID: {exp[0]} | Date: {exp[4]} | Category: {exp[3]} | Amount: Rs.{exp[2]:.2f} | {exp[5]}")
    else:
        print("Failed to insert expenses due to an error. Transaction rolled back.")

if __name__ == "__main__":
    main()
