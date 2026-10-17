import hmac
import os
import secrets
import warnings
from functools import wraps
from urllib.parse import urlparse

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from peewee import DoesNotExist, PeeweeException, fn
from PIL import Image, UnidentifiedImageError
from werkzeug.security import check_password_hash

from models import Place, PlacePhoto, database, initialize_database


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
MAX_IMAGE_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_PHOTOS_PER_PLACE = 8
app.config["MAX_CONTENT_LENGTH"] = (MAX_IMAGE_UPLOAD_BYTES * MAX_PHOTOS_PER_PLACE) + 1024 * 1024

# This safely adds the nullable image column to an existing local database.
initialize_database()

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

DEFAULT_PLACEHOLDER_KEYS = {
    "sightseeing": "temple",
    "food": "noodles",
    "shopping": "crafts",
}
IMAGE_EXTENSIONS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}


def admin_configuration():
    """Read required admin settings without keeping credentials in source code."""
    password_hash = os.environ.get("ADMIN_PASSWORD_HASH")
    return {
        "username": os.environ.get("ADMIN_USERNAME"),
        # A copied hash can accidentally include a line break. Whitespace is
        # not part of a Werkzeug password hash, so remove only its edges.
        "password_hash": password_hash.strip() if password_hash else None,
    }


def csrf_token():
    """Create one random token per browser session for admin forms."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def valid_csrf_token():
    submitted_token = request.form.get("csrf_token", "")
    saved_token = session.get("csrf_token", "")
    return bool(saved_token) and hmac.compare_digest(submitted_token, saved_token)


def require_valid_csrf_token():
    if not valid_csrf_token():
        abort(400, "Your form session has expired. Please try again.")


def admin_required(view_function):
    """Redirect visitors who are not logged in to the separate admin login."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not app.config["SECRET_KEY"]:
            return (
                render_template(
                    "admin_error.html",
                    message="Admin setup is incomplete. Set FLASK_SECRET_KEY and restart the app.",
                ),
                503,
            )
        if not session.get("admin_authenticated"):
            flash("Please log in to access the admin area.", "error")
            return redirect(url_for("admin_login"))
        return view_function(*args, **kwargs)

    return wrapped_view


def get_place_or_none(place_id):
    try:
        return Place.get_by_id(place_id)
    except DoesNotExist:
        return None


def clean_place_form():
    """Validate admin form values before they are saved to the shared Place table."""
    values = {
        "name_en": request.form.get("name_en", "").strip(),
        "name_ja": request.form.get("name_ja", "").strip() or None,
        "category": request.form.get("category", "").strip(),
        "description": request.form.get("description", "").strip(),
        "address": request.form.get("address", "").strip() or None,
        "google_maps_url": request.form.get("google_maps_url", "").strip(),
        "opening_hours": request.form.get("opening_hours", "").strip() or None,
    }
    errors = []

    required_fields = (
        ("name_en", "English name"),
        ("description", "Description"),
        ("google_maps_url", "Google Maps URL"),
    )
    for field_name, label in required_fields:
        if not values[field_name]:
            errors.append(f"{label} is required.")

    if values["category"] not in CATEGORY_LABELS:
        errors.append("Choose a valid category.")

    parsed_url = urlparse(values["google_maps_url"])
    if values["google_maps_url"] and (parsed_url.scheme != "https" or not parsed_url.netloc):
        errors.append("Google Maps URL must be a complete HTTPS URL.")

    if len(values["name_en"]) > 255 or len(values["name_ja"] or "") > 255:
        errors.append("Place names must be 255 characters or fewer.")
    if len(values["opening_hours"] or "") > 255:
        errors.append("Opening hours must be 255 characters or fewer.")

    return values, errors


def attach_photos(places):
    """Add ordered photo lists and a main photo to places for templates."""
    places = list(places)
    photo_lists = {place.id: [] for place in places}
    if photo_lists:
        place_ids = list(photo_lists.keys())
        for photo in (
            PlacePhoto.select()
            .where(PlacePhoto.place.in_(place_ids))
            .order_by(
                PlacePhoto.place,
                PlacePhoto.sort_order,
                PlacePhoto.id,
            )
        ):
            photo_lists[photo.place_id].append(photo)

    for place in places:
        place.photo_list = photo_lists[place.id]
        place.main_photo = place.photo_list[0] if place.photo_list else None
    return places


def ordered_place_photos(place):
    return list(
        PlacePhoto.select().where(PlacePhoto.place == place).order_by(PlacePhoto.sort_order, PlacePhoto.id)
    )


def validate_uploaded_image(image_file):
    """Return a generated filename after validating the uploaded image bytes."""
    if not image_file or not image_file.filename:
        return None, None

    try:
        image_file.stream.seek(0, os.SEEK_END)
        image_size = image_file.stream.tell()
        image_file.stream.seek(0)
    except (AttributeError, OSError):
        return None, "The uploaded image could not be read."

    if image_size > MAX_IMAGE_UPLOAD_BYTES:
        return None, "Image files must be 5 MiB or smaller."

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(image_file.stream) as image:
                image_format = image.format
                image.verify()
    except (
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        OSError,
        UnidentifiedImageError,
        ValueError,
    ):
        return None, "Upload a valid JPG, PNG, or WebP image."
    finally:
        image_file.stream.seek(0)

    extension = IMAGE_EXTENSIONS.get(image_format)
    if extension is None:
        return None, "Upload a JPG, PNG, or WebP image."

    return f"{secrets.token_hex(16)}{extension}", None


def uploaded_image_path(image_filename):
    """Return a path only for a generated filename stored in the database."""
    if not image_filename or image_filename != os.path.basename(image_filename):
        return None
    return os.path.join(UPLOAD_FOLDER, image_filename)


def save_uploaded_image(image_file, image_filename):
    image_path = uploaded_image_path(image_filename)
    if image_path is None:
        raise OSError("Invalid upload filename")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image_file.stream.seek(0)
    image_file.save(image_path)


def remove_uploaded_image_if_unused(image_filename):
    """Remove an upload only when no remaining place record refers to it."""
    image_path = uploaded_image_path(image_filename)
    if image_path is None:
        return
    if PlacePhoto.select().where(PlacePhoto.filename == image_filename).exists():
        return
    if os.path.isfile(image_path):
        os.remove(image_path)


def validate_uploaded_images(image_files):
    uploaded_files = [image_file for image_file in image_files if image_file and image_file.filename]
    if len(uploaded_files) > MAX_PHOTOS_PER_PLACE:
        return [], [f"A place can have at most {MAX_PHOTOS_PER_PLACE} photos."]

    validated_images = []
    errors = []
    for image_file in uploaded_files:
        image_filename, image_error = validate_uploaded_image(image_file)
        if image_error:
            errors.append(image_error)
        else:
            validated_images.append((image_file, image_filename))
    return validated_images, errors


def photo_ids_to_remove(place, submitted_ids):
    existing_photos = {str(photo.id): photo for photo in ordered_place_photos(place)}
    removed_photos = []
    for photo_id in set(submitted_ids):
        photo = existing_photos.get(photo_id)
        if photo is None:
            return [], "A selected photo no longer belongs to this place."
        removed_photos.append(photo)
    return removed_photos, None


def reordered_existing_photos(place, removed_photos, submitted_order):
    removed_ids = {str(photo.id) for photo in removed_photos}
    remaining_photos = [photo for photo in ordered_place_photos(place) if str(photo.id) not in removed_ids]
    by_id = {str(photo.id): photo for photo in remaining_photos}
    ordered_photos = []
    for photo_id in submitted_order.split(","):
        if photo_id and photo_id in by_id and by_id[photo_id] not in ordered_photos:
            ordered_photos.append(by_id[photo_id])
    ordered_photos.extend(photo for photo in remaining_photos if photo not in ordered_photos)
    return ordered_photos


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


@app.route("/")
def home():
    places = attach_photos(Place.select().order_by(fn.Random()))
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
        abort(404)

    places = attach_photos(Place.select().where(Place.category == category))
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
    place = get_place_or_none(place_id)
    if place is None:
        abort(404)

    source_category = request.args.get("from")
    if source_category in CATEGORY_LABELS:
        back_url = url_for("places_by_category", category=source_category)
    else:
        back_url = url_for("home")

    place = attach_photos([place])[0]
    photos = place.photo_list

    return render_template(
        "place_detail.html",
        place=place,
        category_icon=CATEGORY_ICONS[place.category],
        category_label=CATEGORY_LABELS[place.category],
        back_url=back_url,
        photos=photos,
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if not app.config["SECRET_KEY"]:
        return (
            render_template(
                "admin_error.html",
                message="Admin setup is incomplete. Set FLASK_SECRET_KEY and restart the app.",
            ),
            503,
        )

    if session.get("admin_authenticated"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        require_valid_csrf_token()
        configuration = admin_configuration()
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not configuration["username"] or not configuration["password_hash"]:
            flash(
                "Admin configuration is incomplete. Set the required environment variables and restart the app.",
                "error",
            )
        else:
            invalid_password_hash = False
            try:
                password_matches = check_password_hash(configuration["password_hash"], password)
            except ValueError:
                password_matches = False
                invalid_password_hash = True
                flash("Admin password hash configuration is invalid.", "error")

            username_matches = hmac.compare_digest(username, configuration["username"])
            if username_matches and password_matches:
                session.clear()
                session["admin_authenticated"] = True
                flash("You are now logged in.", "success")
                return redirect(url_for("admin_dashboard"))
            elif not invalid_password_hash:
                flash("Invalid username or password.", "error")

    return render_template("admin_login.html", csrf_token=csrf_token())


@app.route("/admin")
@admin_required
def admin_dashboard():
    places = attach_photos(Place.select().order_by(Place.category, Place.name_en))
    return render_template(
        "admin_dashboard.html",
        places=places,
        category_labels=CATEGORY_LABELS,
        csrf_token=csrf_token(),
    )


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    require_valid_csrf_token()
    session.clear()
    flash("You are now logged out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/places/new", methods=["GET", "POST"])
@admin_required
def admin_create_place():
    place_values = {}
    if request.method == "POST":
        require_valid_csrf_token()
        place_values, errors = clean_place_form()
        uploaded_images, image_errors = validate_uploaded_images(request.files.getlist("photos"))
        errors.extend(image_errors)
        if len(uploaded_images) > MAX_PHOTOS_PER_PLACE:
            errors.append(f"A place can have at most {MAX_PHOTOS_PER_PLACE} photos.")
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            place_values["placeholder_key"] = DEFAULT_PLACEHOLDER_KEYS[place_values["category"]]
            saved_filenames = []
            try:
                for image_file, image_filename in uploaded_images:
                    save_uploaded_image(image_file, image_filename)
                    saved_filenames.append(image_filename)
                with database.atomic():
                    place = Place.create(**place_values)
                    for sort_order, (_, image_filename) in enumerate(uploaded_images):
                        PlacePhoto.create(
                            place=place,
                            filename=image_filename,
                            sort_order=sort_order,
                        )
            except (OSError, PeeweeException):
                for image_filename in saved_filenames:
                    remove_uploaded_image_if_unused(image_filename)
                flash("The place could not be added. Please try again.", "error")
                return render_template(
                    "admin_place_form.html",
                    page_title="Add Place",
                    submit_label="Add Place",
                    place=place_values,
                    category_labels=CATEGORY_LABELS,
                    photos=[],
                    csrf_token=csrf_token(),
                )
            flash("Place added successfully.", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin_place_form.html",
        page_title="Add Place",
        submit_label="Add Place",
        place=place_values,
        category_labels=CATEGORY_LABELS,
        photos=[],
        csrf_token=csrf_token(),
    )


@app.route("/admin/places/<int:place_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit_place(place_id):
    place = get_place_or_none(place_id)
    if place is None:
        flash("That place no longer exists.", "error")
        return redirect(url_for("admin_dashboard"))

    place_values = place
    if request.method == "POST":
        require_valid_csrf_token()
        place_values, errors = clean_place_form()
        removed_photos, removal_error = photo_ids_to_remove(place, request.form.getlist("remove_photo"))
        if removal_error:
            errors.append(removal_error)
        uploaded_images, image_errors = validate_uploaded_images(request.files.getlist("photos"))
        errors.extend(image_errors)
        existing_photos = ordered_place_photos(place)
        if len(existing_photos) - len(removed_photos) + len(uploaded_images) > MAX_PHOTOS_PER_PLACE:
            errors.append(f"A place can have at most {MAX_PHOTOS_PER_PLACE} photos.")
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            reordered_photos = reordered_existing_photos(
                place, removed_photos, request.form.get("photo_order", "")
            )
            saved_filenames = []
            try:
                for image_file, image_filename in uploaded_images:
                    save_uploaded_image(image_file, image_filename)
                    saved_filenames.append(image_filename)
                with database.atomic():
                    for field_name, value in place_values.items():
                        setattr(place, field_name, value)
                    place.save()
                    if removed_photos:
                        PlacePhoto.delete().where(
                            PlacePhoto.id.in_([photo.id for photo in removed_photos])
                        ).execute()
                    for sort_order, photo in enumerate(reordered_photos):
                        photo.sort_order = sort_order
                        photo.save()
                    next_sort_order = len(reordered_photos)
                    for image_file, image_filename in uploaded_images:
                        PlacePhoto.create(
                            place=place,
                            filename=image_filename,
                            sort_order=next_sort_order,
                        )
                        next_sort_order += 1
            except (OSError, PeeweeException):
                for image_filename in saved_filenames:
                    remove_uploaded_image_if_unused(image_filename)
                flash("The place could not be updated. Please try again.", "error")
                return render_template(
                    "admin_place_form.html",
                    page_title="Edit Place",
                    submit_label="Save Changes",
                    place=place_values,
                    category_labels=CATEGORY_LABELS,
                    photos=existing_photos,
                    csrf_token=csrf_token(),
                )
            for photo in removed_photos:
                remove_uploaded_image_if_unused(photo.filename)
            flash("Place updated successfully.", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin_place_form.html",
        page_title="Edit Place",
        submit_label="Save Changes",
        place=place_values,
        category_labels=CATEGORY_LABELS,
        photos=ordered_place_photos(place),
        csrf_token=csrf_token(),
    )


@app.route("/admin/places/<int:place_id>/delete", methods=["GET", "POST"])
@admin_required
def admin_delete_place(place_id):
    place = get_place_or_none(place_id)
    if place is None:
        flash("That place no longer exists.", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        require_valid_csrf_token()
        image_filenames = [photo.filename for photo in ordered_place_photos(place)]
        with database.atomic():
            PlacePhoto.delete().where(PlacePhoto.place == place).execute()
            place.delete_instance()
        for image_filename in image_filenames:
            remove_uploaded_image_if_unused(image_filename)
        flash("Place deleted successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_delete_place.html", place=place, csrf_token=csrf_token())


if __name__ == "__main__":
    database.connect(reuse_if_open=True)
    app.run(port=8000, debug=os.environ.get("FLASK_DEBUG") == "1")
