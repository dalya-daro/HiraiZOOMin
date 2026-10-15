# HiraiZOOMin — Database Design

## 1. Table List

| Table | Needed? | Why it is necessary |
| --- | --- | --- |
| `place` | Yes | Stores the information users browse, filter, and view on the place-details page. |

One `Place` table is sufficient for the MVP because every item shown by the app is a place and has the same type of information: name, category, description, map link, and optional practical details.

A `user` table is not needed because there is no login or registration. A separate `category` table is not needed because the app has only three fixed categories: `sightseeing`, `food`, and `shopping`.

## 2. Role of Each Table

### `place`

The `place` table is the app's list of local places in Hiraizumi. Flask will use it to:

- show all places on the home page;
- find places in one category for `/places/<category>`;
- find one place by ID for `/places/<place_id>`; and
- show the place's stored Google Maps search link on the details page.

Each row represents one sightseeing spot, food place, or shopping place.

## 3. Column Name and Data Type

| Column name | SQLite / PeeWee data type | Required? | Information stored |
| --- | --- | --- | --- |
| `id` | `INTEGER` / `AutoField` | Yes | Automatically assigned unique ID for one place. |
| `name_en` | `TEXT` / `CharField` | Yes | English place name shown first to users. |
| `name_ja` | `TEXT` / `CharField(null=True)` | No | Japanese place name, shown below the English name when available. |
| `category` | `TEXT` / `CharField` | Yes | One lowercase fixed value: `sightseeing`, `food`, or `shopping`. |
| `description` | `TEXT` / `TextField` | Yes | Short English description of the place. |
| `placeholder_key` | `TEXT` / `CharField` | Yes | Identifier for the category-based placeholder image or icon, such as `sightseeing`, `food`, or `shopping`. |
| `address` | `TEXT` / `TextField(null=True)` | No | Verified address only; Japanese address text may be included where useful. |
| `google_maps_url` | `TEXT` / `TextField` | Yes | Complete, checked Google Maps search URL for this place. |
| `opening_hours` | `TEXT` / `CharField(null=True)` | No | Verified opening-hours text, such as `09:00–17:00` or `Closed Tuesdays`. |

`CharField` is suitable for short text. `TextField` is suitable for text that may be longer, such as descriptions, addresses, and URLs. In SQLite, both are stored as text, but the PeeWee field choice explains the intended use in the Python model.

The app should only display `address` and `opening_hours` when their values are present. An empty (`NULL`) value means the information is not verified or is not available yet.

## 4. Primary Key

`id` is the primary key. A primary key is a value that uniquely identifies one row in a table.

PeeWee's `AutoField` creates an integer ID automatically for each new place. This ID is used by the details route, for example `/places/3`, to find the correct place. It is more reliable than using a name because two places could have similar names.

## 5. Foreign Key

No foreign keys are needed for the MVP.

A foreign key connects one table to another table. The app does not need that connection because categories are fixed, simple values stored directly in `place.category`. Creating a separate `category` table would add another model, table, and relationship without improving the first version.

The implementation should validate category values so only `sightseeing`, `food`, and `shopping` are used when records are created and when category URLs are requested.

## 6. Unique Constraint

No additional unique constraint is required for the MVP. The primary-key `id` is already unique.

Place names should not be marked unique because different businesses or locations could have the same or similar English name. The Google Maps URL also does not need a unique constraint; the app simply stores the checked link belonging to each place record.

## 7. Index Candidate

`category` is the main index candidate because the Category Results route filters places by this column.

With only six records, an index is not necessary: SQLite can filter this small table immediately. A beginner-friendly first implementation can leave it without a database index. If the app later contains many places and category filtering becomes more frequent, an index on `category` can be added without changing the table design.

The primary-key `id` is automatically indexed, which supports finding a place for `/places/<place_id>`.

## 8. Points to Note When Implementing with PeeWee

- Define one PeeWee model named `Place` that maps to the SQLite `place` table.
- Use `AutoField` for `id`, `CharField` for short required text, and `TextField` for descriptions, addresses, and Google Maps URLs.
- Set `null=True` for optional `name_ja`, `address`, and `opening_hours`. In SQLite, this permits `NULL` when the information has not been verified.
- Keep `name_en`, `category`, `description`, `placeholder_key`, and `google_maps_url` required so every place card and details page has its essential content.
- Connect PeeWee to one local SQLite database file. Create the `place` table during the app's setup or initialization process.
- Use a small seed function to add the six initial records only when the `place` table is empty. This makes it safe to run initialization again without duplicate records.
- Store one complete Google Maps search URL in `google_maps_url` for each sample record. It can be formed from the place name and verified address when available, then checked before use.
- In templates, check whether optional values exist before showing the address or opening-hours section.

## 9. Sample Data Plan

The initial seed data contains exactly six `Place` records:

| Category value | Number of records | Purpose |
| --- | --- | --- |
| `sightseeing` | 2 | Demonstrates sightseeing discovery and category filtering. |
| `food` | 2 | Demonstrates food-place discovery and category filtering. |
| `shopping` | 2 | Demonstrates daily-necessities discovery and category filtering. |

Every sample record will have the required fields: English name, category, short description, placeholder key, and Google Maps search URL. Japanese names, addresses, and opening hours will be added only when they have been verified. The seed plan does not assume an address, opening hours, or checked link for a specific real-world place until that information is confirmed.
