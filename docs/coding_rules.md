# HiraiZOOMin — Coding Rules

## Scope and simplicity

- Build only the agreed MVP plus the separate admin area. Do not add public-user registration, AI, external APIs, embedded maps, GPS navigation, uploads, Blueprints, an application factory, or a CSS framework.
- Prefer concepts already learned. Explain an unfamiliar package or technique, why it is needed, and a simpler alternative before using it.
- Keep the flat project structure: `app.py`, `models.py`, `seed.py`, `templates/`, and `static/`.

## Python style

- Use clear, descriptive `snake_case` names, such as `selected_category`, `place_id`, and `google_maps_url`.
- Keep functions small and focused: routes render pages, model code defines data, and seed code initializes sample data.
- Use constants or one shared collection for the allowed categories; do not repeat category strings in many places.
- Add short comments only when the purpose is not obvious from clear code.

## Flask routes

- Use `GET` for the browsing routes because they display data and do not change it.
- Keep these URL rules: `/`, `/places/<category>`, and `/places/<int:place_id>`.
- Validate route `category` and detail-query `from` values against `sightseeing`, `food`, and `shopping`.
- Use `url_for` for internal links when generating URLs in templates or Python.
- Return `not_found.html` with HTTP status 404 for an invalid category or missing place ID.

## PeeWee and SQLite

- Use one `Place` model and one SQLite database file.
- Store category values only as lowercase `sightseeing`, `food`, or `shopping`; convert them to friendly labels for display.
- Keep `name_en`, `category`, `description`, `placeholder_key`, and `google_maps_url` required.
- Use nullable fields for `name_ja`, `address`, and `opening_hours`; do not fill them with guesses or placeholder facts.
- Create the table if needed, then seed only when the table is empty. Never seed unconditionally.
- Handle a missing record with PeeWee's `DoesNotExist` instead of exposing an error page.

## Templates and optional information

- Reuse one category-results template and one place-details template. Do not make one template per place or category.
- Use Jinja's `{% if value %}` only where optional information may be missing. It means: display the enclosed HTML only when the value exists. Explain this when it is first introduced.
- Show English names first and Japanese names below only when available.
- Let Jinja escape normal database values. Do not use `|safe` for place names, descriptions, addresses, or hours.

## Google Maps links and validation

- Store one complete, owner-verified Google Maps `https` search URL per place.
- Render it as an external link that opens in a new tab; it is not a Flask route.
- Do not use a Google Maps API, embedded map, or unreviewed user-provided link.
- Do not claim a local address, opening hour, or map link is verified unless the project owner has supplied/confirmed it.

## Static placeholders and responsive CSS

- Store placeholder assets under `static/images/` and refer to them through Flask's static-file URL support.
- Do not implement user uploads or create an uploads folder.
- Keep all MVP styling in `static/css/style.css`.
- Use basic responsive CSS only: readable sizes, flexible card layout, and category buttons that wrap on narrow screens. Explain unfamiliar CSS properties when first used.

## Errors and security

- Use a friendly `not_found.html` for invalid categories and missing place IDs, with an HTTP 404 status and a home link.
- Use PeeWee query methods rather than building raw SQL text.
- Validate allowed category values before querying or using them in a back link.
- Keep the local SQLite database, virtual environment, caches, and local environment files out of Git as appropriate.
- Do not expose debug information when the app is shared outside local development.
- Keep the public site login-free. Admin credentials and Flask's secret key must come from environment variables, never source code.
- Use Werkzeug password-hash verification, a server-side admin session check on every management route, CSRF tokens on every admin form, and POST for state-changing actions.
