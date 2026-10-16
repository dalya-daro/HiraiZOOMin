"""Start HiraiZOOMin with temporary admin credentials for this server process."""

import getpass
import os
import secrets
import sys
from pathlib import Path

from werkzeug.security import generate_password_hash


def prompt_for_value(prompt):
    value = input(prompt).strip()
    while not value:
        print("This value cannot be empty.")
        value = input(prompt).strip()
    return value


def prompt_for_password():
    password = getpass.getpass("Admin password: ")
    while not password:
        print("The password cannot be empty.")
        password = getpass.getpass("Admin password: ")
    return password


def configure_environment(username, password):
    """Set credentials only for the Flask process started by this script."""
    os.environ["FLASK_SECRET_KEY"] = secrets.token_urlsafe(32)
    os.environ["ADMIN_USERNAME"] = username
    os.environ["ADMIN_PASSWORD_HASH"] = generate_password_hash(password)


def main():
    print("HiraiZOOMin admin setup")
    username = prompt_for_value("Admin username: ")
    password = prompt_for_password()
    configure_environment(username, password)

    # Replace this helper with Flask so both programs use the same environment.
    app_path = Path(__file__).with_name("app.py")
    os.execv(sys.executable, [sys.executable, str(app_path)])


if __name__ == "__main__":
    main()
