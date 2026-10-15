from flask import Flask, render_template

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
    )


if __name__ == "__main__":
    database.connect()
    app.run(port=8000, debug=True)
