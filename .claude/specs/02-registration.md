# Spec: Registration

## Overview
Implement the user registration feature allowing new users to create an account. This step builds on the database foundation from Step 1 and enables users to sign up with their name, email, and password. Registration is a core prerequisite for the authentication system (Step 3) and all subsequent user-specific features.

## Depends on
- Step 1: Database setup (users table must exist)

## Routes
- POST /register – handles registration form submission – public

## Database changes
No database changes – the users table from Step 1 already contains all required fields (name, email, password_hash).

## Templates
- Modify: `templates/register.html` – add registration form with fields for name, email, password, and password confirmation; include error/success message display

## Files to change
- `app.py` – add POST handler for /register route with form processing logic
- `templates/register.html` – add the registration form
- `static/js/main.js` – add client-side form validation (optional, can do server-side only)

## Files to create
- None

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only – never use string formatting in SQL
- Passwords must be hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables – never hardcode hex values
- All templates extend `base.html`
- Email must be unique – show appropriate error if already registered
- Password and confirm password must match
- All fields (name, email, password) are required
- Display validation errors inline on the registration form

## Definition of Done
- [ ] Registration form displays with fields: name, email, password, confirm password
- [ ] Form submission validates all required fields
- [ ] Duplicate email shows appropriate error message
- [ ] Password mismatch shows error message
- [ ] Successful registration creates user in database with hashed password
- [ ] Successful registration redirects to login page with success message
- [ ] All SQL queries use parameterized statements
- [ ] Form is styled consistently with the application design
- [ ] Password is never stored in plain text
