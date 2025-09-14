import os

import pytest
from flask import Flask, current_app

from flask_maintenance import Maintenance


@pytest.fixture
def app():
    app = Flask(__name__)
    app.route("/")(lambda: "Hello World")
    Maintenance(app)
    return app


@pytest.fixture(autouse=True)
def cleanup_ins_path(app):
    with app.app_context():
        yield app

        try:
            os.rmdir(current_app.instance_path)
        except FileNotFoundError:
            pass


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
