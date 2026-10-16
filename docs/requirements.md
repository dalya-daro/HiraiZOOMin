# HiraiZOOMin — Requirements

## 1. App Overview

HiraiZOOMin is a simple, English-friendly local-discovery web app for foreign visitors and newcomers in Hiraizumi, Japan. It helps users find sightseeing spots, food places, and shops for daily necessities in one place.

The MVP is a small, beginner-friendly learning project built with Python, Flask, PeeWee, and a local SQLite database. It works on smartphones and computers and does not require an account.

The initial database will contain six sample places:

- 2 Sightseeing places
- 2 Food places
- 2 Shopping places

The MVP has three screens:

| Screen | Purpose |
| --- | --- |
| Home / All Places | Introduces the app, provides category controls, and lists all places. |
| Category Results | Shows places for one selected category using the same list layout. |
| Place Details | Shows information for one place and its Google Maps link. |

The public screens do not require login. A separate protected admin area is available for the project owner to manage the same place data; its setup and tests are documented in `docs/admin.md`.

## 2. Target users

**Primary users:** Foreign visitors and newcomers staying in or visiting Hiraizumi, especially people who find local information difficult to discover or understand in English.

Users may not know which places to visit, where to eat, or where to buy daily necessities. Information can be limited, scattered, or difficult to understand, and language barriers can make asking for recommendations difficult.

The interface and descriptions will be primarily in English. Important Japanese place names and Japanese addresses may be shown where they help users identify the correct location.

## 3. Essential features

### Browse all places

- The Home / All Places screen shows the HiraiZOOMin name, a short English introduction, category controls, and all six initial places.
- Each place card shows a category-based placeholder image or icon, name, category, short description, and a **View Details** link or button.

### Filter by category

- Users can view `All Places`, `Sightseeing`, `Food`, or `Shopping`.
- The Category Results screen uses one reusable layout and displays only places in the selected category.
- If no places match, display: “No places available in this category yet.”

### View place details

- Selecting a place opens a reusable Place Details screen for that specific record.
- The page displays the placeholder image/icon, name, category, short description, and verified address and opening hours when available.
- A back link returns users to the relevant Home / All Places or Category Results list they came from.

### Open Google Maps

- Each place has a stored Google Maps search URL.
- The URL can be generated from the place name and address when an address is available.
- The details page provides a clearly labelled **Open in Google Maps** link that opens the stored URL in a new browser tab.
- Each link must be checked to ensure it searches for the intended place.

### Store place data

Use PeeWee with a local SQLite database. Each place record needs the following data:

| Field | Required | Notes |
| --- | --- | --- |
| ID | Yes | Unique database identifier. |
| Name | Yes | Display name; Japanese name may be included where useful. |
| Category | Yes | One of `Sightseeing`, `Food`, or `Shopping`. |
| Short description | Yes | Brief English explanation for visitors. |
| Placeholder image/icon | Yes | Category-based visual used in the MVP. |
| Address | No | Show only when verified; may include Japanese. |
| Google Maps URL | Yes | Google Maps search URL for this place. |
| Opening hours | No | Show only when verified. |

## 4. Features to add if time permits

- Add more verified places.
- Add verified opening hours for more places.
- Replace category placeholders with appropriate local images.
- Add English/Japanese language switching.
- Add useful local categories based on user feedback.

## 5. Non-functional requirements

- Keep the design clean, friendly, and easy to understand for beginner-level English users.
- Use clear category labels and plainly labelled buttons.
- Make the layout responsive and usable on smartphone-sized and desktop-sized browser windows.
- Reuse templates for category lists and place details rather than creating one page for every category or place.
- Keep the project small and achievable for a beginner learning Python, Flask, and PeeWee.

### MVP acceptance checklist

The MVP is ready for review when:

- [ ] The Flask app uses PeeWee with a local SQLite database.
- [ ] The database has six sample records: two per required category.
- [ ] The home page lists all places.
- [ ] Each category filter displays only its matching places.
- [ ] Every listed place opens a working detail page.
- [ ] Each detail page shows the stored information and a Google Maps search link.
- [ ] Each Google Maps link opens in a new tab and has been checked for the intended place.
- [ ] The layout is usable on both a phone-sized and desktop-sized browser window.
- [ ] Public browsing requires no login, external API, embedded map, or advanced feature.
- [ ] The separate `/admin` area requires login and can add, edit, and delete places safely.

## 6. Things to be aware of during implementation

- Do not add public-user accounts, registration, AI features, GPS navigation, embedded or live maps, or external APIs to the MVP. The separate administrator login is the only permitted authentication feature.
- Google Maps is used only through ordinary clickable search URLs; the Google Maps API is not needed.
- Display addresses and opening hours only after they have been verified. Omit information that cannot be confirmed instead of guessing.
- Use simple category-based placeholder images or icons initially, rather than collecting place photos.
- Store a separate Google Maps URL for each place and verify it before including it.
- Keep the data set small at first and add more places only after the core browsing, filtering, details, and map-link functions work.
