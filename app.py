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
    )


if __name__ == "__main__":
    database.connect()
    app.run(port=8000, debug=True)
