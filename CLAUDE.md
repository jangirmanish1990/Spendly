# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Spendly - A Flask-based personal expense tracker web application. This is a student project with features being built incrementally across steps.

## Commands

```bash
# Run the application
python app.py

# Run tests
pytest

# Install dependencies
pip install -r requirements.txt
```

## Architecture

- **Framework**: Flask (Python web framework)
- **Database**: SQLite with foreign key support
- **Frontend**: Vanilla JavaScript, custom CSS (no frameworks)
- **Templating**: Jinja2 HTML templates

### File Structure

```
expense-tracker/
├── app.py              # Flask application, routes
├── database/
│   └── db.py           # Database utilities (get_db, init_db, seed_db)
├── templates/          # Jinja2 HTML templates
├── static/
│   ├── css/style.css   # Application styles
│   └── js/main.js      # Client-side JavaScript
└── tests/              # pytest test files
```

### Key Components

- **`app.py`**: Main Flask application with routes for landing, auth (login/register), and placeholder routes for expenses CRUD
- **`database/db.py`**: SQLite database layer - must implement `get_db()`, `init_db()`, `seed_db()`
- **`templates/base.html`**: Base template with navbar, footer, and Google Fonts (DM Serif Display, DM Sans)
- **`static/css/style.css`**: CSS variables for theming, responsive design

### Development Pattern

Features are built incrementally:
- Step 1: Database setup
- Step 3: Authentication (login/logout)
- Step 4: User profile
- Step 7-9: Expense CRUD operations
