# Spec: Add Expense

## Overview
Step 7 lets a logged-in user record a new expense. The `/expenses/add` route stub
already exists in `app.py`; this step replaces it with a real GET/POST handler.
The GET renders a blank expense form. The POST validates the submitted data,
inserts a new row into the `expenses` table, and redirects to `/profile` with a
success flash. An "Add Expense" button is added to the profile page so users can
reach the form without typing the URL directly.

## Depends on
- Step 1: Database setup (`expenses` table must exist)
- Step 3: Auth (session must carry `user_id`)
- Step 4: Profile page (`templates/profile.html` must exist to add the Add Expense button)

## Routes
- `GET  /expenses/add` — render blank add-expense form — logged-in only
- `POST /expenses/add` — validate and insert new expense, then redirect — logged-in only

## Database changes
No database changes. All required columns (`user_id`, `amount`, `category`, `date`,
`description`) already exist in the `expenses` table.

## Templates
- **Create:** `templates/add_expense.html`
  - Extends `base.html`
  - A single card-style form with fields: Amount, Category (dropdown), Date, Description
  - Amount: `<input type="number" step="0.01" min="0.01">`
  - Category: `<select>` with options Food, Transport, Bills, Health, Entertainment, Shopping, Other
  - Date: `<input type="date">` — default value set to today's date
  - Description: `<input type="text">` (optional)
  - Submit button labelled "Add Expense"
  - Cancel link back to `/profile`
  - Re-populate all fields from submitted values on failed POST validation
  - Display flash messages (errors) inline above the form

- **Modify:** `templates/profile.html`
  - Add an "Add Expense" button/link near the Transaction History section heading
  - Points to `url_for('add_expense')`

## Files to change
- `app.py`
  - Replace the `add_expense` stub with a GET/POST handler:
    - Auth guard: redirect to login if not logged-in
    - GET: render `add_expense.html` with today's date pre-filled
    - POST: read and validate `amount`, `category`, `date`, `description`;
      on error re-render form with flash messages and submitted values;
      on success insert row into `expenses` and redirect to `/profile` with
      a success flash

- `database/db.py`
  - Add one new helper function:
    - `add_expense(user_id, amount, category, date, description)` — executes
      the `INSERT` and commits

- `templates/profile.html`
  - Add "Add Expense" button near Transaction History heading (see Templates)

- `static/css/style.css`
  - Add any styles needed for the add-expense form card that aren't already
    covered by `.auth-card`, `.form-group`, `.form-input`, `.btn-submit`, `.btn-ghost`

## Files to create
- `templates/add_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline styles
- The logged-in user's `user_id` must come from `session["user_id"]` — never
  from a form field
- Amount validation: must be a positive number > 0; reject zero and negative values
- Category validation: must be one of the seven allowed values (Food, Transport,
  Bills, Health, Entertainment, Shopping, Other); reject anything else
- Date validation: must parse as `YYYY-MM-DD` via `datetime.strptime`; reject
  malformed or missing dates
- Description is optional — store `None` when blank
- On POST validation failure, re-render the form with the submitted values so the
  user does not have to retype everything
- Today's date default must be computed in `app.py` using `datetime.now()`, not
  hardcoded or computed in the template

## Definition of done
- [ ] `GET /expenses/add` renders a blank form with today's date pre-filled
- [ ] Submitting valid data inserts a new expense and redirects to `/profile` with a success flash
- [ ] The new expense appears in the profile transaction table immediately after submission
- [ ] The profile page shows an "Add Expense" button that navigates to the form
- [ ] Submitting an amount ≤ 0 re-renders the form with a validation error
- [ ] Submitting a blank or malformed date re-renders the form with a validation error
- [ ] Submitting an invalid category re-renders the form with a validation error
- [ ] A logged-out user visiting `/expenses/add` is redirected to `/login`
- [ ] All form fields retain the last-submitted values when validation fails (no blank form on error)
- [ ] Description field can be left empty and the expense is saved successfully
