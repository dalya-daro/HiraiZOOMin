# HiraiZOOMin — Routing Design

## Overview

HiraiZOOMin uses three simple Flask `GET` routes. `GET` is appropriate because each route only displays information; it does not create, edit, or delete data.

The app uses one reusable template for category results and one reusable template for place details. It does not need a separate route or template for each category or place.

## Route table

| Route name / purpose | URL rule | HTTP method | Purpose and behavior | Template to render | Parameters and query parameters | Possible destination or screen transitions |
| --- | --- | --- | --- | --- | --- | --- |
| Home / All Places | `/` | `GET` | Displays the app introduction, category controls, and all six initial places. | `home.html` | None | Category buttons go to `/places/sightseeing`, `/places/food`, or `/places/shopping`. A place's details link goes to `/places/<place_id>`. |
| Category Results | `/places/<category>` | `GET` | Validates the requested category, then displays places in that category using a reusable results layout. Supported values are `sightseeing`, `food`, and `shopping`. | `places.html` | **Route parameter:** `category`, the category word in the URL. | All Places and back links go to `/`. Category buttons go to another supported category URL. A place's details link goes to `/places/<place_id>?from=<category>`. |
| Place Details | `/places/<int:place_id>` | `GET` | Finds and displays one place, including its description, verified practical information, and Google Maps link. | `place_detail.html` | **Route parameter:** `place_id`, the numeric database ID. **Optional query parameter:** `from`, the originating category, such as `food`. | Back link goes to `/places/<from>` when `from` is valid; otherwise it goes to `/`. Google Maps opens externally in a new tab. |

## Category validation

The category route must accept only these category values:

- `sightseeing`
- `food`
- `shopping`

If the URL contains another value, the app should handle it clearly and safely. A beginner-friendly choice is to show a simple “Category not found” page with a link back to `/`; returning a 404 response is also suitable.

## Detail-page and back-link behavior

The `place_id` identifies the selected place record in the SQLite database. For example, `/places/3` displays the place whose ID is `3`.

The optional `from` query parameter tells the details page which list the user came from:

- `/places/3?from=food` returns to `/places/food`
- `/places/3?from=sightseeing` returns to `/places/sightseeing`
- `/places/3?from=shopping` returns to `/places/shopping`
- `/places/3` has no `from` value and returns to `/`

The app should validate `from` against the three supported category values. If it is missing or invalid, use `/` as the safe back-link destination.

If no place exists for the requested `place_id`, handle it gracefully by rendering a simple not-found page or returning a 404 response rather than showing an error to the user.

## Google Maps links

Google Maps links are ordinary external hyperlinks, not Flask routes. Each place record stores its own Google Maps search URL. The URL can be generated from the place name and verified address when an address is available.

The link opens in a new browser tab and does not use the Google Maps API, an embedded map, or another external API.
