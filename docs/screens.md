
HiraiZOOMin — Screen Mockup Specification
Overview
The Day 8 MVP has three screens:

Main screen — browse all places and choose a category.
Filtered results screen — view places matching the selected category.
Place details screen — read information about one selected place.
The app should work without AI or external APIs. Use sample place data and local images or placeholders.

Screen 1: Main Screen (Initial Screen)
Purpose: Let users browse available places and choose whether to see all places, sightseeing spots, or food.

Components (top to bottom)
App name / logo
Example: HiraiZOOMin
Welcome heading
Example: Explore Hiraizumi!
Short description
Example: Discover places to visit and food to try.
Category buttons
All
Sightseeing
Food
List of places
Each item contains:
Photo or placeholder image
Place name, e.g. Chusonji Temple
Category, e.g. Sightseeing
Short description, e.g. A famous historic temple in Hiraizumi.
Button: View Details
Optional bottom navigation
Keep only if needed; it is not required for the MVP.
Main interactions
Selecting All shows all sample places.
Selecting Sightseeing opens Screen 2 with sightseeing results.
Selecting Food opens Screen 2 with food results.
Selecting View Details opens Screen 3 for that place.
Main screen: This is the first screen the user interacts with.

Relevant buttons: All, Sightseeing, Food, and each item's View Details button.

Screen 2: Filtered Results Screen
Purpose: Show only places matching the category selected on Screen 1.

Components (top to bottom)
Back button
Example: ← Back to All Places
Screen heading
Example: Sightseeing in Hiraizumi or Food in Hiraizumi
Short description
Example for sightseeing: Explore historic temples and beautiful spots.
Example for food: Find local food and restaurants to try.
List of matching places
Each item contains:
Photo or placeholder image
Place name, e.g. Motsuji Temple
Category, e.g. Sightseeing
Short description, e.g. A beautiful temple with a large garden.
Button: View Details
Main interactions
The selected category determines which places appear.
Selecting View Details opens Screen 3 for that place.
Selecting Back to All Places returns to Screen 1.
Screen 3: Place Details Screen
Purpose: Give the user enough information about one place to help decide whether to visit it.

Components (top to bottom)
Back button
Example: ← Back to Places
Place photo
Place name
Example: Chusonji Temple
Category label
Example: Sightseeing
Description
Example: Chusonji Temple is a historic temple in Hiraizumi, known for its beautiful grounds and Konjikido Hall.
Location or address
Example label: Address
Display a verified address if available in the sample data.
Optional opening hours
Example label: Opening Hours
Include only if the information has been checked; otherwise omit it.
Back button
Example: Back to Places
Main interactions
The screen displays information for the place selected on Screen 1 or Screen 2.
The back button returns the user to the previous list screen.
User Navigation Flow
Screen 1: Main Screen
  ├─ Select “All” → show all places
  ├─ Select “Sightseeing” → Screen 2: Filtered Results
  ├─ Select “Food” → Screen 2: Filtered Results
  └─ Select “View Details” → Screen 3: Place Details

Screen 2: Filtered Results
  ├─ Select “View Details” → Screen 3: Place Details
  └─ Select “Back to All Places” → Screen 1

Screen 3: Place Details
  └─ Select “Back to Places” → return to the previous list
MVP Notes
Use a small set of sample places and restaurants.
Store sample data directly in the app at first.
Use local images or placeholders.
Do not require login, user registration, AI, or external APIs.
Build and test the main screen first, then category filtering, then place details.
Verify addresses and opening hours before displaying them; omit unverified information.
