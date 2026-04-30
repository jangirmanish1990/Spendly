import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "spendly-secret-key-change-in-production")


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If already logged in, redirect to landing
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        # Get form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html", error="All fields are required.")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return render_template("register.html", error="Password must be at least 8 characters.")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html", error="Passwords do not match.")

        # Check if email already exists
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash("Email already registered. Please sign in.", "error")
            return render_template("register.html", error="Email already registered.")

        # Hash password and insert user
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("login"))

    # GET request
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, redirect to landing
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        # Get form data
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html", error="Email and password are required.")

        # Look up user by email
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and password matches
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html", error="Invalid email or password.")

        from werkzeug.security import check_password_hash
        if not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html", error="Invalid email or password.")

        # Success - store user info in session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("profile"))

    # GET request - render login form
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    # Clear session
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("landing"))


def parse_date(value):
    """Validate and return ISO date string or None if malformed."""
    if not value or not value.strip():
        return None
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return value.strip()
    except ValueError:
        return None


def get_summary_stats(cursor, user_id, date_from=None, date_to=None):
    """Fetch summary stats (total spent, transaction count, top category) with optional date filter."""
    # Build date filter clause
    date_clause = ""
    params = [user_id]
    if date_from and date_to:
        date_clause = "AND date >= ? AND date <= ?"
        params = [user_id, date_from, date_to]
    elif date_from:
        date_clause = "AND date >= ?"
        params = [user_id, date_from]
    elif date_to:
        date_clause = "AND date <= ?"
        params = [user_id, date_to]

    # Total spent
    cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? {date_clause}", params)
    total_spent = cursor.fetchone()[0]

    # Transaction count
    cursor.execute(f"SELECT COUNT(*) FROM expenses WHERE user_id = ? {date_clause}", params)
    transaction_count = cursor.fetchone()[0]

    # Top category
    cursor.execute(f"""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ? {date_clause}
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """, params)
    top_category_row = cursor.fetchone()
    top_category = top_category_row["category"] if top_category_row else "N/A"

    return {
        "total_spent": total_spent,
        "transaction_count": transaction_count,
        "top_category": top_category
    }


def get_recent_transactions(cursor, user_id, limit=5, date_from=None, date_to=None):
    """Fetch recent transactions with optional date filter."""
    date_clause = ""
    params = [user_id]
    if date_from and date_to:
        date_clause = "AND date >= ? AND date <= ?"
        params = [user_id, date_from, date_to]
    elif date_from:
        date_clause = "AND date >= ?"
        params = [user_id, date_from]
    elif date_to:
        date_clause = "AND date <= ?"
        params = [user_id, date_to]

    cursor.execute(f"""
        SELECT id, date, description, category, amount
        FROM expenses
        WHERE user_id = ? {date_clause}
        ORDER BY date DESC
        LIMIT {limit}
    """, params)
    rows = cursor.fetchall()

    return [
        {
            "date": row["date"],
            "description": row["description"],
            "category": row["category"],
            "amount": row["amount"]
        }
        for row in rows
    ]


def get_category_breakdown(cursor, user_id, date_from=None, date_to=None):
    """Fetch category breakdown with percentages and optional date filter."""
    date_clause = ""
    params = [user_id]
    if date_from and date_to:
        date_clause = "AND date >= ? AND date <= ?"
        params = [user_id, date_from, date_to]
    elif date_from:
        date_clause = "AND date >= ?"
        params = [user_id, date_from]
    elif date_to:
        date_clause = "AND date <= ?"
        params = [user_id, date_to]

    # First get total for percentage calculation
    cursor.execute(f"""
        SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? {date_clause}
    """, params)
    total_spent = cursor.fetchone()[0]

    # Get category amounts
    cursor.execute(f"""
        SELECT category, SUM(amount) as amount
        FROM expenses
        WHERE user_id = ? {date_clause}
        GROUP BY category
        ORDER BY amount DESC
    """, params)
    category_rows = cursor.fetchall()

    categories = []
    if total_spent > 0:
        for row in category_rows:
            percentage = round((row["amount"] / total_spent) * 100)
            categories.append({
                "name": row["category"],
                "amount": row["amount"],
                "percentage": percentage
            })

    return categories


@app.route("/profile")
def profile():
    # Require authentication
    if not session.get("user_id"):
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get and validate date filter parameters from query string
    date_from = parse_date(request.args.get("date_from", ""))
    date_to = parse_date(request.args.get("date_to", ""))

    # Handle invalid date range: flash error and fall back to no filter
    if date_from and date_to and date_from > date_to:
        flash("Start date must be before end date.", "error")
        date_from = None
        date_to = None

    # Compute preset dates for quick-select buttons
    today = datetime.now().strftime("%Y-%m-%d")
    this_month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")

    three_months_ago = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

    # Determine active preset for UI highlighting
    active_preset = None
    if date_from == this_month_start and date_to == today:
        active_preset = "this_month"
    elif date_from == three_months_ago and date_to == today:
        active_preset = "last_3_months"
    elif date_from == six_months_ago and date_to == today:
        active_preset = "last_6_months"
    elif not date_from and not date_to:
        active_preset = "all_time"

    conn = get_db()
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    user = {
        "name": user_row["name"],
        "email": user_row["email"],
        "member_since": user_row["created_at"][:10] if user_row else "Unknown"
    }

    # Fetch data using helper functions
    stats = get_summary_stats(cursor, user_id, date_from, date_to)
    transactions = get_recent_transactions(cursor, user_id, limit=5, date_from=date_from, date_to=date_to)
    categories = get_category_breakdown(cursor, user_id, date_from, date_to)

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
        date_from=date_from or "",
        date_to=date_to or "",
        active_preset=active_preset,
        this_month_start=this_month_start,
        three_months_ago=three_months_ago,
        six_months_ago=six_months_ago,
        today=today
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
