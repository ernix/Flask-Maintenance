from flask_maintenance.cli import maintenance as maintenance_cli


def test_default_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_maintenance_commands(client, runner):
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
