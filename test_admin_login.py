import os
import re
import unittest
from unittest.mock import patch

from werkzeug.security import check_password_hash, generate_password_hash

import app as application
from start_app import configure_environment


class AdminLoginTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(
            os.environ,
            {
                "ADMIN_USERNAME": "test-admin",
                "ADMIN_PASSWORD_HASH": generate_password_hash("test-password"),
            },
        )
        self.environment.start()
        application.app.config.update(
            TESTING=True,
            SECRET_KEY="temporary-test-secret",
        )
        self.client = application.app.test_client()

    def tearDown(self):
        self.environment.stop()

    def csrf_token(self):
        response = self.client.get("/admin/login")
        match = re.search(r'name="csrf_token" value="([^"]+)"', response.get_data(as_text=True))
        return match.group(1)

    def test_correct_credentials_log_in(self):
        response = self.client.post(
            "/admin/login",
            data={
                "csrf_token": self.csrf_token(),
                "username": "test-admin",
                "password": "test-password",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/admin"))

    def test_incorrect_password_fails(self):
        response = self.client.post(
            "/admin/login",
            data={
                "csrf_token": self.csrf_token(),
                "username": "test-admin",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid username or password.", response.get_data(as_text=True))

    def test_incorrect_username_fails(self):
        response = self.client.post(
            "/admin/login",
            data={
                "csrf_token": self.csrf_token(),
                "username": "wrong-admin",
                "password": "test-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid username or password.", response.get_data(as_text=True))

    def test_missing_csrf_token_is_rejected(self):
        response = self.client.post(
            "/admin/login",
            data={"username": "test-admin", "password": "test-password"},
        )

        self.assertEqual(response.status_code, 400)

    def test_admin_logout_endpoint_is_registered_for_post(self):
        self.assertIn("admin_logout", application.app.view_functions)
        logout_rules = [
            rule
            for rule in application.app.url_map.iter_rules()
            if rule.endpoint == "admin_logout"
        ]

        self.assertEqual(len(logout_rules), 1)
        self.assertEqual(logout_rules[0].rule, "/admin/logout")
        self.assertEqual(logout_rules[0].methods, {"POST", "OPTIONS"})

    def test_logout_requires_csrf_token_and_clears_authenticated_session(self):
        with self.client.session_transaction() as test_session:
            test_session["admin_authenticated"] = True
            test_session["csrf_token"] = "test-csrf-token"

        rejected_response = self.client.post("/admin/logout")
        self.assertEqual(rejected_response.status_code, 400)

        response = self.client.post(
            "/admin/logout",
            data={"csrf_token": "test-csrf-token"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/admin/login"))
        with self.client.session_transaction() as test_session:
            self.assertNotIn("admin_authenticated", test_session)

    def test_hash_with_accidental_edge_whitespace_still_works(self):
        with patch.dict(
            os.environ,
            {"ADMIN_PASSWORD_HASH": generate_password_hash("test-password") + "\n"},
        ):
            response = self.client.post(
                "/admin/login",
                data={
                    "csrf_token": self.csrf_token(),
                    "username": "test-admin",
                    "password": "test-password",
                },
            )

        self.assertEqual(response.status_code, 302)

    def test_startup_helper_creates_matching_temporary_credentials(self):
        with patch.dict(os.environ, {}, clear=False):
            configure_environment("helper-admin", "helper-password")

            self.assertEqual(os.environ["ADMIN_USERNAME"], "helper-admin")
            self.assertTrue(os.environ["FLASK_SECRET_KEY"])
            self.assertTrue(
                check_password_hash(
                    os.environ["ADMIN_PASSWORD_HASH"],
                    "helper-password",
                )
            )


if __name__ == "__main__":
    unittest.main()
