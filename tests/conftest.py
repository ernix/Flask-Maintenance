import os

import pytest
from flask import Blueprint, Flask, Response, current_app


@pytest.fixture
def app():
    app = Flask(__name__, static_folder=None)
    app.route("/")(lambda: "Hello World")
    app.add_url_rule(
        "/static/style.css",
        endpoint="static",
        view_func=lambda: Response(
            "body{background-color:black;}",
            mimetype="text/css",
        ),
    )
    bp = Blueprint("bp", __name__, url_prefix="/bp", static_folder=None)
    bp.add_url_rule(
        "/static/substyle.css",
        endpoint="static",
        view_func=lambda: Response(
            "body{background-color:black;}",
            mimetype="text/css",
        ),
    )
    app.register_blueprint(bp)
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
