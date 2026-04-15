from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
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
    # If already logged in, redirect to profile
    if session.get("user_id"):
        return redirect(url_for("profile"))

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


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


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
