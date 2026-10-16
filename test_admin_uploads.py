import io
import os
import tempfile
import unittest

from PIL import Image

import app as application
from models import Place, database, initialize_database


class AdminImageUploadTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.original_database = database.database
        self.original_upload_folder = application.UPLOAD_FOLDER
        self.original_max_content_length = application.app.config["MAX_CONTENT_LENGTH"]

        database.close()
        database.init(os.path.join(self.temporary_directory.name, "test.db"))
        initialize_database()
        application.UPLOAD_FOLDER = os.path.join(self.temporary_directory.name, "uploads")
        application.app.config.update(
            TESTING=True,
            SECRET_KEY="temporary-test-secret",
            MAX_CONTENT_LENGTH=application.MAX_IMAGE_UPLOAD_BYTES + 1024 * 1024,
        )
        self.client = application.app.test_client()
        with self.client.session_transaction() as test_session:
            test_session["admin_authenticated"] = True
            test_session["csrf_token"] = "test-csrf-token"

    def tearDown(self):
        database.close()
        database.init(self.original_database)
        application.UPLOAD_FOLDER = self.original_upload_folder
        application.app.config["MAX_CONTENT_LENGTH"] = self.original_max_content_length
        self.temporary_directory.cleanup()

    def form_data(self, **overrides):
        values = {
            "csrf_token": "test-csrf-token",
            "name_en": "Upload Test Place",
            "name_ja": "",
            "category": "food",
            "description": "A test place with an uploaded image.",
            "placeholder_key": "noodles",
            "address": "",
            "google_maps_url": "https://www.google.com/maps/search/?api=1&query=test",
            "opening_hours": "",
        }
        values.update(overrides)
        return values

    def image_upload(self, image_format="PNG"):
        image_bytes = io.BytesIO()
        Image.new("RGB", (20, 20), "green").save(image_bytes, format=image_format)
        image_bytes.seek(0)
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[image_format]
        return image_bytes, f"untrusted-name.{extension}"

    def create_uploaded_place(self):
        response = self.client.post(
            "/admin/places/new",
            data={**self.form_data(), "image": self.image_upload()},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 302)
        return Place.get(Place.name_en == "Upload Test Place")

    def test_successful_upload_uses_generated_filename_and_public_pages(self):
        place = self.create_uploaded_place()

        self.assertRegex(place.image_filename, r"^[0-9a-f]{32}\.png$")
        self.assertTrue(os.path.isfile(os.path.join(application.UPLOAD_FOLDER, place.image_filename)))
        self.assertIn(
            f"uploads/{place.image_filename}",
            self.client.get("/").get_data(as_text=True),
        )
        self.assertIn(
            f"uploads/{place.image_filename}",
            self.client.get(f"/places/{place.id}").get_data(as_text=True),
        )

    def test_unsupported_image_content_is_rejected(self):
        gif_bytes = io.BytesIO(
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        )
        response = self.client.post(
            "/admin/places/new",
            data={**self.form_data(), "image": (gif_bytes, "pretend.jpg")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Upload a JPG, PNG, or WebP image.", response.get_data(as_text=True))
        self.assertEqual(Place.select().count(), 0)

    def test_oversized_image_is_rejected(self):
        oversized_image = io.BytesIO(b"x" * (application.MAX_IMAGE_UPLOAD_BYTES + 1))
        response = self.client.post(
            "/admin/places/new",
            data={**self.form_data(), "image": (oversized_image, "large.png")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Image files must be 5 MiB or smaller.", response.get_data(as_text=True))
        self.assertEqual(Place.select().count(), 0)

    def test_edit_without_replacement_keeps_existing_image(self):
        place = self.create_uploaded_place()
        image_filename = place.image_filename

        response = self.client.post(
            f"/admin/places/{place.id}/edit",
            data=self.form_data(description="Updated without replacing the image."),
        )

        self.assertEqual(response.status_code, 302)
        place = Place.get_by_id(place.id)
        self.assertEqual(place.image_filename, image_filename)
        self.assertTrue(os.path.isfile(os.path.join(application.UPLOAD_FOLDER, image_filename)))

    def test_replacing_image_removes_unused_old_file(self):
        place = self.create_uploaded_place()
        old_image_filename = place.image_filename

        response = self.client.post(
            f"/admin/places/{place.id}/edit",
            data={
                **self.form_data(),
                "image": self.image_upload("JPEG"),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 302)
        place = Place.get_by_id(place.id)
        self.assertNotEqual(place.image_filename, old_image_filename)
        self.assertTrue(os.path.isfile(os.path.join(application.UPLOAD_FOLDER, place.image_filename)))
        self.assertFalse(os.path.exists(os.path.join(application.UPLOAD_FOLDER, old_image_filename)))

    def test_deleting_place_removes_its_unused_uploaded_image(self):
        place = self.create_uploaded_place()
        image_path = os.path.join(application.UPLOAD_FOLDER, place.image_filename)

        response = self.client.post(
            f"/admin/places/{place.id}/delete",
            data={"csrf_token": "test-csrf-token"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Place.select().where(Place.id == place.id).exists())
        self.assertFalse(os.path.exists(image_path))


if __name__ == "__main__":
    unittest.main()
