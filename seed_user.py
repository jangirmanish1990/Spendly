#!/usr/bin/env python3
"""Seed a single realistic Indian user into the database."""

import sqlite3
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE = "spendly.db"


# Common Indian first names by region
INDIAN_FIRST_NAMES = [
    # North Indian
    "Rahul", "Amit", "Rajesh", "Suresh", "Vikram", "Arjun", "Nikhil", "Rohan",
    "Priya", "Anjali", "Sneha", "Pooja", "Ritu", "Kavita", "Deepika", "Shruti",
    # South Indian
    "Aravind", "Karthik", "Pradeep", "Ramesh", "Ganesh", "Krishnan", "Balaji",
    "Lakshmi", "Meera", "Divya", "Shalini", "Kavya", "Anitha", "Ramya",
    # East/West Indian
    "Sourav", "Anirban", "Debasish", "Partha", "Siddharth", "Kunal", "Vishal",
    "Rituparna", "Ishita", "Aishwarya", "Nandini", "Manasi", "Tejaswi",
    # Pan-Indian Muslim names
    "Ayaan", "Zayan", "Rehan", "Faizan", "Sameer", "Imran",
    "Ayesha", "Fatima", "Zara", "Nadia", "Sana", "Mariam"
]

INDIAN_LAST_NAMES = [
    # North Indian
    "Sharma", "Verma", "Gupta", "Agarwal", "Singh", "Kumar", "Yadav", "Malhotra",
    "Kapoor", "Chopra", "Bhatia", "Sethi", "Khanna", "Mittal",
    # South Indian
    "Iyer", "Iyengar", "Menon", "Nair", "Reddy", "Rao", "Chetty", "Pillai",
    "Gowda", "Hegde", "Kulkarni", "Deshmukh", "Patil",
    # East/West Indian
    "Banerjee", "Chatterjee", "Mukherjee", "Das", "Ganguly", "Bose",
    "Joshi", "Deshpande", "Oak", "Parekh", "Shah", "Patel", "Mehta"
]


def get_db():
    """Opens connection to SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def generate_unique_email():
    """Generate a unique email that doesn't exist in the database."""
    max_attempts = 50
    conn = get_db()
    cursor = conn.cursor()

    for _ in range(max_attempts):
        first_name = random.choice(INDIAN_FIRST_NAMES)
        last_name = random.choice(INDIAN_LAST_NAMES)
        number_suffix = random.randint(10, 99)

        # Create email: firstname.lastnameNN@gmail.com
        email = f"{first_name.lower()}.{last_name.lower()}{number_suffix}@gmail.com"

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone() is None:
            conn.close()
            return email, first_name, last_name

    conn.close()
    raise Exception("Could not generate unique email after multiple attempts")


def seed_user():
    """Generate and insert a random Indian user into the database."""
    # Generate unique user
    email, first_name, last_name = generate_unique_email()
    full_name = f"{first_name} {last_name}"
    password_hash = generate_password_hash("password123")
    created_at = datetime.now().isoformat()

    # Insert into database
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (full_name, email, password_hash, created_at)
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Print confirmation
    print(f"User created successfully!")
    print(f"  id: {user_id}")
    print(f"  name: {full_name}")
    print(f"  email: {email}")


if __name__ == "__main__":
    seed_user()
