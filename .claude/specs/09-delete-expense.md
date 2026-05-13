# Spec: Delete Expense

## Overview
Step 9 lets a logged-in user permanently delete an expense record from the profile page.
A "Delete" button appears alongside the existing "Edit" link on each row of the recent
transactions table. Clicking it submits an inline POST form which triggers a browser
confirmation dialog before sending the request. The `/expenses/<id>/delete` route
verifies the user owns the expense, deletes the row, flashes a success message, and
redirects back to `/profile`. Ownership is enforced — attempting to delete another
user's expense returns a 403.

## Depends on
- Step 1: Database setup (`expenses` table must exist)
- Step 3: Auth (session must carry `user_id`)
- Step 4: Profile page (`templates/profile.html` transaction table must exist)
- Step 8: Edit Expense (`get_expense_by_id` helper must exist in `database/db.py`)

## Routes
- `POST /expenses/<int:id>/delete` — delete the expense and redirect to profile — logged-in only

## Database changes
No database changes. The `expenses` table already supports row deletion.

## Templates
- **Create:** None

- **Modify:** `templates/profile.html`
  - In the recent-transactions table actions column, add an inline `<form method="POST">`
    pointing to `url_for('delete_expense', id=txn.id)`
  - The form contains a single `<button type="submit">` labelled "Delete"
  - The form has an `onsubmit="return confirm('Delete this expense?')"` guard so the
    browser shows a confirmation dialog before submitting

## Files to change
- `app.py`
  - Add the `delete_expense` route handler:
    - Auth guard: redirect to login if not logged-in
    - Fetch expense by `id` via `get_expense_by_id`; if not found return 404; if
      `user_id` mismatches return 403
    - Call `delete_expense` db helper and commit
    - Flash "Expense deleted." success message
    - Redirect to `/profile`
  - Import `delete_expense` from `database.db` (alias as `delete_expense_db` to avoid
    name collision with the route function)

- `database/db.py`
  - Add `delete_expense(expense_id)` helper — executes `DELETE FROM expenses WHERE id = ?`
    and commits

- `templates/profile.html`
  - Add Delete button form to each transaction row in the actions column

- `static/css/style.css`
  - Add `.btn-danger` and `.btn-sm` styles for the delete button
  - Add `.inline-form` utility to display the form inline (no block layout disruption)
  - Use CSS variables — never hardcode hex values

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Delete route must only accept POST — never GET
- Ownership check must happen before the DELETE is executed
- Return HTTP 403 (not a redirect) when ownership check fails
- Return HTTP 404 when the expense `id` does not exist
- Browser confirmation dialog must be present (`onsubmit` confirm) — do not skip it
- Route function name must be `delete_expense`; import the db helper under a different
  alias (`delete_expense_db`) to avoid the name collision

## Definition of done
- [ ] A "Delete" button appears on every row in the profile recent-transactions table
- [ ] Clicking Delete shows a browser confirmation dialog before submitting
- [ ] Confirming the dialog deletes the expense from the database and redirects to `/profile`
- [ ] A success flash message "Expense deleted." appears after deletion
- [ ] The deleted expense no longer appears in the transactions table after redirect
- [ ] Cancelling the confirmation dialog does not delete the expense
- [ ] A logged-out user POSTing to the delete URL is redirected to `/login`
- [ ] POSTing to a non-existent expense ID returns a 404 response
- [ ] A logged-in user attempting to delete another user's expense receives a 403 response
