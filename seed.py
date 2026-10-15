from models import Place, database, initialize_database


ALLOWED_CATEGORIES = ["sightseeing", "food", "shopping"]

# Add six owner-verified place dictionaries here before running the seed script.
# Do not include "id" because PeeWee creates it automatically.
# Each dictionary needs these fields:
# name_en, name_ja, category, description, placeholder_key, address,
# google_maps_url, opening_hours

SAMPLE_PLACES = [
    {
        "name_en": "Sakura Heritage Temple",
        "name_ja": None,
        "category": "sightseeing",
        "description": "A peaceful temple surrounded by green trees, offering visitors a glimpse of traditional Japanese architecture.",
        "placeholder_key": "temple",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Sakura+Heritage+Temple",
        "opening_hours": None,
    },
    {
        "name_en": "Maple Garden",
        "name_ja": None,
        "category": "sightseeing",
        "description": "A quiet garden with a small pond, seasonal flowers, and scenic walking paths.",
        "placeholder_key": "garden",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Maple+Garden",
        "opening_hours": None,
    },
    {
        "name_en": "Little Noodle House",
        "name_ja": None,
        "category": "food",
        "description": "A cozy restaurant serving warm noodle soup and simple Japanese comfort food.",
        "placeholder_key": "noodles",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Little+Noodle+House",
        "opening_hours": None,
    },
    {
        "name_en": "Rice Ball Corner",
        "name_ja": None,
        "category": "food",
        "description": "A small takeaway shop offering rice balls with different fillings for travelers on the go.",
        "placeholder_key": "onigiri",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Rice+Ball+Corner",
        "opening_hours": None,
    },
    {
        "name_en": "Little Craft Shop",
        "name_ja": None,
        "category": "shopping",
        "description": "A small shop featuring handmade crafts, pottery, and gifts inspired by Japanese culture.",
        "placeholder_key": "crafts",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Little+Craft+Shop",
        "opening_hours": None,
    },
    {
        "name_en": "Sweet Memories",
        "name_ja": None,
        "category": "shopping",
        "description": "A souvenir shop selling packaged sweets and small gifts to take home.",
        "placeholder_key": "sweets",
        "address": None,
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Sweet+Memories",
        "opening_hours": None,
    },
]


def sample_data_is_valid():
    if len(SAMPLE_PLACES) != 6:
        print("Add exactly six verified sample places before seeding.")
        return False

    category_counts = {
        "sightseeing": 0,
        "food": 0,
        "shopping": 0,
    }

    for place_data in SAMPLE_PLACES:
        required_fields = [
            "name_en",
            "name_ja",
            "category",
            "description",
            "placeholder_key",
            "address",
            "google_maps_url",
            "opening_hours",
        ]

        for field_name in required_fields:
            if field_name not in place_data:
                print(f"Missing field: {field_name}")
                return False

        if place_data["category"] not in ALLOWED_CATEGORIES:
            print(f"Invalid category: {place_data['category']}")
            return False

        category_counts[place_data["category"]] += 1

    for category in ALLOWED_CATEGORIES:
        if category_counts[category] != 2:
            print(f"Add exactly two places in the {category} category.")
            return False

    return True


def seed_places():
    initialize_database()
    database.connect()

    if Place.select().exists():
        print("Place records already exist. No records were added.")
    elif sample_data_is_valid():
        for place_data in SAMPLE_PLACES:
            Place.create(
                name_en=place_data["name_en"],
                name_ja=place_data["name_ja"],
                category=place_data["category"],
                description=place_data["description"],
                placeholder_key=place_data["placeholder_key"],
                address=place_data["address"],
                google_maps_url=place_data["google_maps_url"],
                opening_hours=place_data["opening_hours"],
            )
        print("Six sample places were added.")

    database.close()


if __name__ == "__main__":
    seed_places()
