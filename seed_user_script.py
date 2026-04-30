"""Seed a realistic random Indian user into the database."""
import random
import sys
sys.path.insert(0, '.')

from database.db import get_db
from werkzeug.security import generate_password_hash

# Common Indian first names (across regions and religions)
FIRST_NAMES = [
    # North Indian
    "Rahul", "Rajesh", "Amit", "Suresh", "Rakesh", "Vikram", "Ajay", "Manoj",
    "Priya", "Neha", "Pooja", "Ritu", "Sneha", "Anjali", "Kavita", "Deepika",
    # South Indian
    "Arjun", "Karthik", "Venkat", "Krishnan", "Balaji", "Raghavan", "Prakash",
    "Lakshmi", "Meena", "Revathi", "Padmavati", "Kamala", "Sarala", "Bharathi",
    # Pan-India modern names
    "Aryan", "Rohan", "Aditya", "Siddharth", "Nikhil", "Abhishek", "Varun",
    "Ananya", "Diya", "Ishita", "Kavya", "Riya", "Shruti", "Tanvi",
    # Muslim names common in India
    "Arif", "Farhan", "Imran", "Kamran", "Salman", "Tariq", "Yusuf",
    "Ayesha", "Fatima", "Nazia", "Sana", "Tasneem", "Yasmin", "Zainab"
]

LAST_NAMES = [
    # North Indian
    "Sharma", "Verma", "Gupta", "Agarwal", "Singh", "Kumar", "Yadav", "Malhotra",
    "Kapoor", "Chopra", "Bhatia", "Sethi", "Arora", "Jain", "Bansal", "Goyal",
    # South Indian
    "Iyer", "Iyengar", "Menon", "Nair", "Reddy", "Rao", "Chetty", "Gounder",
    "Pillai", "Nambiar", "Hegde", "Shenoy", "Kamath", "Prabhu", "Desai",
    # Pan-India
    "Patel", "Thakur", "Chauhan", "Rajput", "Bhatt", "Joshi", "Pandey", "Tiwari",
    "Mishra", "Dubey", "Srivastava", "Saxena", "Khanna", "Mehra", "Sood",
    # Muslim surnames
    "Ansari", "Qureshi", "Khan", "Pathan", "Siddiqui", "Mirza", "Baig"
]

def generate_name():
    """Generate a realistic Indian name."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"

def generate_email(name):
    """Generate email from name with random digits."""
    parts = name.lower().split()
    firstname = parts[0]
    lastname = parts[1] if len(parts) > 1 else "user"
    digits = random.randint(10, 999)
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = random.choice(domains)
    return f"{firstname}.{lastname}{digits}@{domain}"

def check_email_exists(email):
    """Check if email already exists in database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def seed_user():
    """Generate and insert a unique random Indian user."""
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        name = generate_name()
        email = generate_email(name)

        if not check_email_exists(email):
            break
        attempt += 1
    else:
        print(f"Warning: Could not generate unique email after {max_attempts} attempts")
        return

    # Hash password
    password_hash = generate_password_hash("password123")

    # Insert user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    conn.commit()

    # Get the new user's id
    user_id = cursor.lastrowid
    conn.close()

    # Print confirmation
    print(f"User created successfully!")
    print(f"  id: {user_id}")
    print(f"  name: {name}")
    print(f"  email: {email}")
    print(f"  password: password123")

if __name__ == "__main__":
    seed_user()
