# HiraiZOOMin — Implementation Tasks

Complete tasks in order. Keep database checks separate from routes and templates so problems are easier to find.

## 1. Prepare the local environment

- **Priority:** P0
- **Implement:** Create/activate a virtual environment and make Flask and PeeWee available. Keep the database file out of Git.
- **Done when:** Python can import Flask and PeeWee in the project environment.
- **Check:** Run a short import check or start a minimal Flask app without an import error.

## 2. Create the database connection and `Place` model

- **Priority:** P0
- **Implement:** Add the SQLite connection and one PeeWee `Place` model with the fields in `docs/database.md`.
- **Done when:** The model has required name, category, description, placeholder, and map-link fields; Japanese name, address, and opening hours are nullable.
- **Check:** Inspect the model and confirm the three allowed category values are documented/validated.

## 3. Create the `place` table

- **Priority:** P0
- **Implement:** Add initialization that creates the SQLite table if it does not already exist.
- **Done when:** A local database exists and contains a `place` table.
- **Check:** Run initialization twice; the second run completes without a table-creation error.

## 4. Add safe seed initialization

- **Priority:** P0
- **Implement:** Add a seed function that inserts records only when the `place` table is empty.
- **Done when:** Initialization can be run repeatedly without duplicate records.
- **Check:** Run it twice and confirm the record count is unchanged after the second run.

## 5. Add the six owner-provided sample records

- **Priority:** P0
- **Implement:** Add two verified records in each category using information supplied by the project owner.
- **Done when:** The database has exactly six records: two `sightseeing`, two `food`, and two `shopping`.
- **Check:** Query all records and query each category separately. Do not add unverified addresses, hours, or map links.

## 6. Build the home route and all-places query

- **Priority:** P1
- **Implement:** Add `GET /` and retrieve all places from the database.
- **Done when:** The route renders `home.html` with all six records.
- **Check:** Open `/` in a browser and confirm each place shows its English name, category, description, placeholder, and details link.

## 7. Build the shared place-list template

- **Priority:** P1
- **Implement:** Create the reusable place-card/list markup used by the home and category pages.
- **Done when:** English names appear first and Japanese names appear below only when available.
- **Check:** Confirm a record without `name_ja` does not show an empty Japanese-name line.

## 8. Add category filtering

- **Priority:** P1
- **Implement:** Add `GET /places/<category>` with one reusable results template and a PeeWee category filter.
- **Done when:** Each supported category lists only its two matching records; invalid categories return a 404 page.
- **Check:** Open all three category URLs and an invalid URL such as `/places/unknown`.

## 9. Build place details

- **Priority:** P1
- **Implement:** Add `GET /places/<int:place_id>` and render `place_detail.html` for one database record.
- **Done when:** A detail page shows the intended record and missing optional fields are hidden with a simple Jinja `{% if %}` conditional.
- **Check:** Open a valid place ID and confirm no blank address/opening-hours labels are displayed.

## 10. Add relevant back links and Google Maps links

- **Priority:** P1
- **Implement:** Pass `from=<category>` from category pages to details; use it for the detail-page back link. Render each stored map URL as an external new-tab link.
- **Done when:** Details opened from a category return to that category; details opened from home return to `/`; map links open separately.
- **Check:** Test one details link from home and one from every category. Test each owner-verified Google Maps URL.

## 11. Add 404 handling

- **Priority:** P1
- **Implement:** Create `not_found.html` and use it for invalid category values and nonexistent place IDs.
- **Done when:** Both cases return the page with HTTP status 404 and a link to home.
- **Check:** Open `/places/invalid` and a nonexisting numeric place URL.

## 12. Add basic responsive styling and placeholders

- **Priority:** P2
- **Implement:** Add `static/css/style.css` and static category placeholder assets under `static/images/`.
- **Done when:** Cards are readable, category buttons wrap on narrow screens, and links/buttons are easy to tap.
- **Check:** Resize the browser to phone width and desktop width; inspect all three screens.

## 13. Complete final MVP testing

- **Priority:** P2
- **Implement:** Test the requirements acceptance checklist end to end.
- **Done when:** Browsing, filtering, details, back links, map links, missing optional data, and 404 handling all work with six records.
- **Check:** Use the checklist in `docs/requirements.md` and record any issue before adding optional improvements.

## 14. Manage places through the separate admin area

- **Priority:** P1
- **Implement:** Configure administrator credentials through environment variables, then use the protected `/admin` routes to add, edit, and delete the existing `Place` records.
- **Done when:** Public browsing remains login-free; every admin management route requires an authenticated server-side session; every admin form uses CSRF protection; deletion requires a confirmation POST.
- **Check:** Follow the manual checks in `docs/admin.md`, including unauthenticated redirects, invalid form data, and CSRF rejection.
