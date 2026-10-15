# HiraiZOOMin — AI Context

## App overview

HiraiZOOMin is an English-friendly local-discovery web app for foreign visitors and newcomers in Hiraizumi, Japan. It helps users discover sightseeing spots, food places, and shops for daily necessities. English is the main interface language; Japanese place names and verified addresses may be shown where useful.

The MVP contains six real-world sample places: two each in `sightseeing`, `food`, and `shopping`. The project owner will provide and verify the place information and Google Maps links. AI must not invent or claim to verify local information.

## Technologies and structure

- Python, Flask, PeeWee, and SQLite
- No external APIs or Google Maps API; Google Maps uses ordinary external search links
- No login, registration, AI features, GPS navigation, embedded maps, or image uploads

Use this flat structure:

```text
app.py
models.py
seed.py
templates/
static/
  css/style.css
  images/
docs/
```

Do not introduce Blueprints, an application factory, or a CSS framework for the MVP.

## Implemented features versus planned features

### Implemented

No application features have been implemented yet. The requirements, screen design, route design, database design, and AI guidance documents are planning documents only.

### Planned MVP

- SQLite database with one `Place` table and six seed records
- Home page at `/` listing all places
- Category pages at `/places/sightseeing`, `/places/food`, and `/places/shopping`
- Place details at `/places/<place_id>`, with an optional `from` query parameter for the back link
- Stored Google Maps links that open in a new tab
- Simple `not_found.html` page with HTTP 404 responses for invalid categories and missing place IDs
- Category-based placeholder images/icons and basic responsive CSS

## What we have learned so far

- **Python:** variables, lists/dictionaries, conditions and loops, functions, exceptions, classes, and importing project files
- **Flask:** routes, route IDs, GET/POST methods, templates, loops in templates, forms, redirects, `url_for`, and local development server settings
- **PeeWee:** SQLite databases, models and `Meta`, fields, table creation, create/select/filter/order queries, lookup by ID, saving, deleting, and `DoesNotExist`
- **Other:** virtual environments, pip, requirements files, Git, assertions, `.env` files, and calling APIs with `requests`

## Things I haven't learned yet

- Template inheritance and `base.html`
- Jinja `{% if %}` conditionals
- Static files and CSS
- Flash messages
- Login, sessions, password hashing, and CSRF protection
- File uploads
- Table relationships and `ForeignKeyField`
- Blueprints and more complex project organization
- Libraries other than Flask and PeeWee

## Requests to AI

- Prefer learned concepts and a small amount of clear code over advanced patterns.
- Before using an unfamiliar package or technique, explain what it is, why it is needed, and the simpler alternative; get confirmation before proceeding.
- Simple Jinja `{% if %}` conditionals and one basic CSS file are approved. Explain them when first implementing them.
- Keep each change focused and verify it with a beginner-friendly check.
- Do not expand the MVP, change routes/database fields, or add dependencies without permission.
- Preserve existing user changes and do not claim an unimplemented feature works.

## Decisions that must not change without asking

- One `Place` table; no `User` or `Category` table
- Allowed database category values: `sightseeing`, `food`, `shopping`
- Six initial records, supplied and verified by the project owner
- Home route `/` is the only All Places page
- Reusable templates for category results and details
- Optional address and opening-hours values are nullable and shown only when verified
- Each place stores its own complete, checked Google Maps URL
- Detail pages use an optional `from` value for the relevant back-link destination
- Invalid categories and missing place IDs use `not_found.html` with HTTP 404
- Placeholders are static assets; user-uploaded images are out of scope
