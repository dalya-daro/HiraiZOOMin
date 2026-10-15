from flask import Flask, render_template

from models import database


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    database.connect()
    app.run(port=8000, debug=True)
