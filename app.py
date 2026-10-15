from flask import Flask, render_template, request, url_for
from peewee import DoesNotExist

from models import Place, database


app = Flask(__name__)

CATEGORY_ICONS = {
    "sightseeing": "🏯",
    "food": "🍽️",
    "shopping": "🛍️",
}

CATEGORY_LABELS = {
    "sightseeing": "Sightseeing",
    "food": "Food",
    "shopping": "Shopping",
}


@app.route("/")
def home():
    places = list(Place.select())
    return render_template(
        "home.html",
        places=places,
        category_icons=CATEGORY_ICONS,
        category_labels=CATEGORY_LABELS,
        page_heading="All Places",
        empty_message="No places available yet. Please check back later.",
        source_category=None,
    )


@app.route("/places/<category>")
def places_by_category(category):
    if category not in CATEGORY_LABELS:
        return "Category not found.", 404

    places = list(Place.select().where(Place.category == category))
    return render_template(
        "home.html",
        places=places,
        category_icons=CATEGORY_ICONS,
        category_labels=CATEGORY_LABELS,
        page_heading=f"{CATEGORY_LABELS[category]} in Hiraizumi",
        empty_message="No places available in this category yet.",
        source_category=category,
    )


@app.route("/places/<int:place_id>")
def place_detail(place_id):
    try:
        place = Place.get_by_id(place_id)
    except DoesNotExist:
        return "Place not found.", 404

    source_category = request.args.get("from")
    if source_category in CATEGORY_LABELS:
        back_url = url_for("places_by_category", category=source_category)
    else:
        back_url = url_for("home")

    return render_template(
        "place_detail.html",
        place=place,
        category_icon=CATEGORY_ICONS[place.category],
        category_label=CATEGORY_LABELS[place.category],
        back_url=back_url,
    )


if __name__ == "__main__":
    database.connect()
    app.run(port=8000, debug=True)
