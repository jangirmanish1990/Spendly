# Spec: Backend Routes for Profile Page

## Overview

This step wires up the profile page to fetch real data from the database instead of using hardcoded values. The profile route will query the `users` and `expenses` tables to display actual user information, transaction history, spending statistics, and category breakdowns. This transforms the static UI from Step 04 into a fully functional feature connected to the data layer.

## Depends on

- Step 1: Database setup (users and expenses tables exist)
- Step 2: Registration (users can create accounts)
- Step 3: Login + Logout (session management works)
- Step 4: Profile Page (UI template is complete)

## Routes

- `GET /profile` — render profile page with real database data — logged-in only

No new routes — just modify the existing `/profile` handler.

## Database changes

No database changes. The existing `users` and `expenses` tables from Step 1 are sufficient.

## Templates

- **Modify:** `templates/profile.html` — no changes expected; the template already accepts dynamic data via context variables

## Files to change

- `app.py` — update the `/profile` route to:
  - Fetch user data from `users` table using `session.get("user_id")`
  - Calculate summary stats (total spent, transaction count, top category) from `expenses` table
  - Fetch recent transactions for the transaction history table
  - Calculate category breakdown with percentages

## Files to create

- None

## New dependencies

- No new dependencies

## Rules for implementation

- No SQLAlchemy or ORMs — use raw sqlite3 via `get_db()`
- Parameterised queries only — never string-format SQL
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Authentication guard: check `session.get("user_id")`; if absent, `redirect(url_for("login"))`
- All monetary values should be formatted to 2 decimal places
- Dates should be displayed in YYYY-MM-DD format
- Category breakdown percentages should add up to ~100%
- Handle edge cases: user with no expenses should still see the profile page

## Definition of done

- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] Logged-in user sees their actual name and email from the database
- [ ] Summary stats (total spent, transaction count, top category) reflect real expense data
- [ ] Transaction history table shows actual expenses from the database (at least 5 most recent)
- [ ] Category breakdown shows real spending by category with correct percentages
- [ ] Demo user (demo@spendly.com) can log in and see their 8 seeded expenses
- [ ] All SQL queries use parameterized statements
- [ ] No hardcoded data remains in the profile route
- [ ] Profile page handles users with zero expenses gracefully
