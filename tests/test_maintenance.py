from flask_maintenance import Maintenance
from flask_maintenance.cli import maintenance as maintenance_cli


def test_default_index(app, client):
    Maintenance(app)
    response = client.get("/")
    assert response.status_code == 200


def test_maintenance_commands(app, client, runner):
    Maintenance(app)
    result = runner.invoke(maintenance_cli, args=["enable"])
    assert result.exit_code == 0
    assert "maintenance mode enabled." in result.output

    response = client.get("/")
    assert response.status_code == 503

    result = runner.invoke(maintenance_cli, args=["disable"])
    assert result.exit_code == 0
    assert "maintenance mode disabled." in result.output

    response = client.get("/")
    assert response.status_code == 200


def test_static_files(app, client, runner):
    Maintenance(app)
    result = runner.invoke(maintenance_cli, args=["enable"])
    assert result.exit_code == 0
    assert "maintenance mode enabled." in result.output

    response = client.get("/static/style.css")
    assert response.status_code == 200

    result = runner.invoke(maintenance_cli, args=["disable"])
    assert result.exit_code == 0
    assert "maintenance mode disabled." in result.output

    response = client.get("/")
    assert response.status_code == 200


def test_blueprint_static_files(app, client, runner):
    Maintenance(app)
    result = runner.invoke(maintenance_cli, args=["enable"])
    assert result.exit_code == 0
    assert "maintenance mode enabled." in result.output

    response = client.get("/bp/static/substyle.css")
    assert response.status_code == 200

    result = runner.invoke(maintenance_cli, args=["disable"])
    assert result.exit_code == 0
    assert "maintenance mode disabled." in result.output

    response = client.get("/")
    assert response.status_code == 200


def test_lock_filename_option(app, client, runner):
    Maintenance(app, lock_filename="lock")
    result = runner.invoke(maintenance_cli, args=["enable"])
    assert result.exit_code == 0
    assert "maintenance mode enabled." in result.output

    response = client.get("/")
    assert response.status_code == 503

    result = runner.invoke(maintenance_cli, args=["disable"])
    assert result.exit_code == 0
    assert "maintenance mode disabled." in result.output

    response = client.get("/")
    assert response.status_code == 200


def test_redirect(app, client, runner):
    Maintenance(app)
    result = runner.invoke(
        maintenance_cli, args=["enable", "--redirect", "https://example.com/"]
    )
    assert result.exit_code == 0
    assert "maintenance mode enabled." in result.output

    response = client.get("/")
    assert response.status_code == 302
    assert response.location == "https://example.com/"

    result = runner.invoke(maintenance_cli, args=["disable"])
    assert result.exit_code == 0
    assert "maintenance mode disabled." in result.output

    response = client.get("/")
    assert response.status_code == 200
