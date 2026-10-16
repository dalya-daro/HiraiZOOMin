# HiraiZOOMin — Screen Design

## Overview

HiraiZOOMin has three screens for its MVP. It helps foreign visitors and newcomers discover sightseeing, food, and shopping places in Hiraizumi. The interface is primarily in English, with Japanese place names and addresses shown where useful.

The public screens do not require login, registration, or an account. A separate admin area requires an administrator login and is documented in `docs/admin.md`. The app uses category-based placeholder images or icons in the first version.

## 1. Home / All Places

### Purpose

Welcome users to HiraiZOOMin and let them browse all available places. This is the only All Places screen.

| Item | Design |
| --- | --- |
| Login required | No |
| URL | `/` |
| HTTP method | `GET` |
| Flask template | `home.html` |

### Components

- App name: **HiraiZOOMin**
- Welcome heading, such as “Explore Hiraizumi!”
- Short English introduction to sightseeing, food, and shopping places
- Horizontal category buttons: **All Places**, **Sightseeing**, **Food**, and **Shopping**
- A responsive list of all available place cards

Each place card displays:

- Category-based placeholder image or icon
- English place name
- Japanese place name below the English name, when available
- Category label
- Short English description
- **View Details** link or button

### Main user interactions

- Select **All Places** to remain on or return to `/`.
- Select **Sightseeing**, **Food**, or **Shopping** to open the selected Category Results screen.
- Select **View Details** to open that place's Place Details screen. The link includes no `from` value when opened from the home page.

### Screen transitions

- Users reach this screen by opening `/`, using the All Places button, or using a details-page back link when that place was opened from home.
- Users can move to `/places/sightseeing`, `/places/food`, `/places/shopping`, or `/places/<place_id>`.

## 2. Category Results

### Purpose

Show only places in the category selected by the user. One reusable template handles all three supported categories.

| Item | Design |
| --- | --- |
| Login required | No |
| URL | `/places/<category>` where category is `sightseeing`, `food`, or `shopping` |
| HTTP method | `GET` |
| Flask template | `places.html` |

### Components

- Back link: **← All Places**, leading to `/`
- Category heading, such as “Sightseeing in Hiraizumi”
- Short category description
- The same horizontal category buttons used on the home screen
- Responsive list of matching place cards
- Friendly empty-state message: “No places available in this category yet.” when no places match

Each matching place card displays:

- Category-based placeholder image or icon
- English place name
- Japanese place name below the English name, when available
- Category label
- Short English description
- **View Details** link or button

### Main user interactions

- Select a category button to change the displayed category.
- Select **All Places** or the back link to return to `/`.
- Select **View Details** to open the selected place at `/places/<place_id>?from=<category>`.

### Screen transitions

- Users reach this screen from a category button on Home / All Places or another Category Results screen.
- Users can return to `/`, choose another category URL, or open a matching place's details page.

## 3. Place Details

### Purpose

Show enough information about one place for a user to decide whether to visit it and to find it through Google Maps.

| Item | Design |
| --- | --- |
| Login required | No |
| URL | `/places/<place_id>`; optional query parameter, for example `/places/3?from=food` |
| HTTP method | `GET` |
| Flask template | `place_detail.html` |

### Components

- Back link
  - Returns to `/places/<from>` when `from` is a valid originating category
  - Returns to `/` when no `from` parameter is supplied
- Category-based placeholder image or icon
- English place name
- Japanese place name below the English name, when available
- Category label
- Short English description
- Verified address when available, including Japanese address where useful
- Verified opening hours when available
- Clearly labelled **Open in Google Maps** external link

### Main user interactions

- Select the back link to return to the relevant list.
- Select **Open in Google Maps** to open the place's stored Google Maps search link in a new browser tab.

### Screen transitions

- Users reach this screen from Home / All Places or Category Results.
- The back link returns to `/` for a place opened from Home / All Places, or to `/places/sightseeing`, `/places/food`, or `/places/shopping` for a place opened from that category list.
- The Google Maps link opens an external Google Maps search page; it is not a HiraiZOOMin screen or Flask route.

## Responsive layout notes

- Category buttons appear in a horizontal row when space allows and wrap neatly on narrow screens.
- Place cards use a single-column layout on small screens and can use multiple columns on wider screens.
- Text, buttons, and links must remain easy to read and tap on a phone.
