# HiraiZOOMin Admin Area

The public guide does not require an account. Place management is available only in the separate `/admin` area.

## Start the app securely on Windows Git Bash

Run this one command from the project folder:

```bash
python start_app.py
```

The helper prompts for an admin username and password without echoing the password. It generates a new Flask secret key and a Werkzeug password hash in Python, places them in the process environment, then starts `app.py` using that same environment. It never writes or prints the password, password hash, or secret key.

Keep that Git Bash terminal open while using the app. To change the credentials, stop Flask with `Ctrl+C` and run `python start_app.py` again.

This replaces manual `export` and `.env` setup. Those methods were unreliable here because a password hash can be altered while passing through shell commands, and a Flask process cannot see environment variables added after it starts.

## Admin routes

| URL | Methods | Login required | Purpose |
| --- | --- | --- | --- |
| `/admin/login` | `GET`, `POST` | No | Shows the admin login form and starts an admin session after valid credentials. |
| `/admin/logout` | `POST` | Yes | Ends the admin session. |
| `/admin` | `GET` | Yes | Lists places and links to management actions. |
| `/admin/places/new` | `GET`, `POST` | Yes | Adds a place to the existing `Place` table. |
| `/admin/places/<place_id>/edit` | `GET`, `POST` | Yes | Updates a place. |
| `/admin/places/<place_id>/delete` | `GET`, `POST` | Yes | Shows a confirmation page, then deletes only after a confirmed POST. |

Every form includes a session-bound CSRF token. All management routes check the server-side session; an unauthenticated request is redirected to `/admin/login`.

## Place images

When adding a place, an authenticated administrator can optionally select a local JPG, JPEG, PNG, or WebP image. The file is checked from its actual image content, not just its name or browser-reported type, and must be 5 MiB or smaller. HiraiZOOMin generates its own filename and stores that filename in the database; image files themselves are stored locally in `static/uploads/`.

On the edit page, the current uploaded image is shown. Leave the file field empty to keep it, or choose a replacement image. A replacement or deleted place removes its old upload only after the database update succeeds and only when no remaining place uses that filename. Existing places without uploads continue to use their bundled placeholder images.

These are local server files, not cloud storage. Uploaded images should be backed up with the application files, and the uploads folder should not be copied between unrelated deployments without its matching database records.

## Running and manual testing

1. In Git Bash, run `python start_app.py`. Do not start a second Flask server from another terminal.
2. Open `http://127.0.0.1:8000/` and confirm the public place pages work without login and show no admin links.
3. Open `http://127.0.0.1:8000/admin`; confirm it redirects to `/admin/login`.
4. Try an incorrect login, then log in using the configured username and password.
5. Add a place using a permitted category and an HTTPS Google Maps URL. Optionally choose a JPG, PNG, or WebP image no larger than 5 MiB. Confirm it appears in `/` and its category page.
6. Edit the place without selecting an image and confirm the current image remains. Then optionally replace it and confirm the public details change.
7. Open its delete page, choose Cancel, then repeat and confirm deletion. Confirm the record and its unused uploaded image disappear from the public pages.
8. Log out and confirm `/admin`, create, edit, and delete URLs all redirect to the login page.
9. Submit a saved form again after changing or removing its hidden CSRF token; it must not change data.

Only enter place information and Google Maps URLs that the project owner has supplied and verified.
