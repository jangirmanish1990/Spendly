# Spec: Edit Expense

## Overview
Step 8 lets a logged-in user edit an existing expense record. The `/expenses/<id>/edit`
route stub already exists in `app.py`; this step replaces that stub with a real
GET/POST handler. The GET renders a pre-filled edit form. The POST validates the
submitted data, updates the row, and redirects the user back to `/profile` with a
success flash. Ownership is enforced — a user who attempts to edit another user's
expense receives a 403. An "Edit" link on each row of the profile transaction table
drives users to this form.

## Depends on
- Step 1: Database setup (`expenses` table must exist)
- Step 3: Auth (session must carry `user_id`)
- Step 4: Profile page (`templates/profile.html` transaction table must exist to add the edit link)

## Routes
- `GET  /expenses/<int:id>/edit` — render pre-filled edit form — logged-in only
- `POST /expenses/<int:id>/edit` — validate and persist the update, then redirect — logged-in only

## Database changes
No database changes. All required columns (`amount`, `category`, `date`,
`description`) already exist in the `expenses` table.

## Templates
- **Create:** `templates/edit_expense.html`
  - Extends `base.html`
  - A single card-style form with fields: Amount, Category (dropdown), Date, Description
  - Amount: `<input type="number" step="0.01" min="0.01">`
  - Category: `<select>` with options Food, Transport, Bills, Health, Entertainment, Shopping, Other
  - Date: `<input type="date">`
  - Description: `<input type="text">` (optional)
  - Submit button labelled "Save Changes"
  - Cancel link back to `/profile`
  - Re-populate all fields from the expense object on GET and on failed POST validation
  - Display flash messages (errors) inline above the form

- **Modify:** `templates/profile.html`
  - In the recent-transactions table, add an "Edit" link per row that points to
    `url_for('edit_expense', id=transaction.id)`
  - Requires `get_recent_transactions` to include the `id` field in each row dict

## Files to change
- `app.py`
  - Replace the `edit_expense` stub with a GET/POST handler:
    - Auth guard: redirect to login if not logged-in
    - Fetch expense by `id`; if not found return 404; if `user_id` mismatches return 403
    - GET: render `edit_expense.html` pre-filled with the expense data
    - POST: read and validate `amount`, `category`, `date`, `description`; on error
      re-render the form with flash messages; on success execute `UPDATE` and
      redirect to `/profile` with a success flash

- `database/db.py`
  - Expose two new helper functions:
    - `get_expense_by_id(expense_id)` — returns the row as a dict or `None`
    - `update_expense(expense_id, amount, category, date, description)` — executes
      the `UPDATE` and commits

- `templates/profile.html`
  - Add Edit link/button to each row in the recent-transactions table (see Templates)

- `static/css/style.css`
  - Add styles for the edit-expense form card (reuse existing form/card CSS variables
    where possible; add only what is missing)

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline styles
- Ownership check must happen in `app.py` before any data is returned or mutated —
  fetch the row first, then compare `row["user_id"]` to `session["user_id"]`
- Return HTTP 403 (not a redirect) when ownership check fails
- Return HTTP 404 when the expense `id` does not exist
- Amount validation: must be a positive number > 0; reject zero and negative values
- Category validation: must be one of the seven allowed values; reject anything else
- Date validation: must parse as `YYYY-MM-DD` via `datetime.strptime`; reject malformed
- Description is optional — store empty string as `None` (or allow empty TEXT)
- On POST validation failure, re-render the form with the submitted values so the user
  does not have to retype everything
- The profile transaction table must include the `id` field in each row dict returned
  by `get_recent_transactions`; add `id` to the SELECT and the returned dict

## Definition of done
- [ ] `GET /expenses/<id>/edit` renders a form pre-filled with the correct expense data
- [ ] Submitting valid changes updates the expense in the database and redirects to `/profile` with a success flash
- [ ] The profile recent-transactions table shows an "Edit" link for each row
- [ ] Submitting an amount ≤ 0 re-renders the form with a validation error
- [ ] Submitting a blank or malformed date re-renders the form with a validation error
- [ ] Submitting an invalid category re-renders the form with a validation error
- [ ] A logged-out user visiting the edit URL is redirected to `/login`
- [ ] Requesting an expense that does not exist returns a 404 response
- [ ] A logged-in user attempting to edit another user's expense receives a 403 response
- [ ] All form fields retain the last-submitted values when validation fails (no blank form on error)
