# Spec: Login and Logout

## Overview

This step implements user authentication for the Spendly expense tracker. Users can log in with their email and password (created during Step 2 registration) and log out securely. Session management uses Flask's built-in session with secure cookies. This feature is essential before building user-specific features like profile management and expense CRUD operations.

## Depends on

- Step 01: Database setup (users table exists)
- Step 02: Registration (users can create accounts)

## Routes

- `POST /login` — Process login form submission — public
- `GET /logout` — Clear session and redirect to landing — logged-in users only
- `GET /login` — Already exists (Step 02), renders login form

## Database changes

No database changes. The users table created in Step 01 is sufficient.

## Templates

- **Create:** `templates/login.html` — Login form with email and password fields, link to registration page
- **Modify:** None (login route already exists in app.py, just needs template)

## Files to change

- `app.py` — Implement POST /login handler, implement /logout with session management

## Files to create

- `templates/login.html` — Login form template

## New dependencies

No new dependencies. Uses Flask sessions and existing werkzeug.security for password verification.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only (use ? placeholders)
- Passwords verified with werkzeug.security.check_password_hash()
- Use CSS variables — never hardcode hex values
- All templates extend base.html
- Use Flask session for authentication state
- Flash appropriate messages for success/error states
- Redirect logged-in users away from /login to /profile

## Definition of done

- [ ] Login form renders at /login with email and password fields
- [ ] Valid credentials log user in and redirect to /profile
- [ ] Invalid credentials show error message and stay on login page
- [ ] Empty/missing fields show validation error
- [ ] Logout clears session and redirects to landing page
- [ ] Logged-in users accessing /login are redirected to /profile
- [ ] Flash messages display appropriately (success on login, confirmation on logout)
- [ ] All templates extend base.html and use existing CSS variables
