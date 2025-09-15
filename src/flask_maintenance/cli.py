import os
import click
import json
from flask import current_app
from flask.cli import with_appcontext


@click.group()
def maintenance():
    """Enable or disable Maintenance mode."""
    pass


@maintenance.command()
@click.option("--redirect", default=None, help="Redirect all requests, instead of 503")
@with_appcontext
def enable(redirect):
    """
    Enable Maintenance mode.
    """
    _path = current_app.extensions['maintenance'].lock_filepath()
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    try:
        with open(_path, 'w') as fp:
            json.dump(dict(redirect=redirect), fp)
    except Exception as e:  # pragma: no cover
        click.echo(e)
        return False

    click.echo('maintenance mode enabled.')
    return True


@maintenance.command()
@with_appcontext
def disable():
    """
    Disable Maintenance mode.
    """
    _path = current_app.extensions['maintenance'].lock_filepath()
    try:
        os.remove(_path)
    except Exception as e:  # pragma: no cover
        click.echo(e)
        return False
    else:
        click.echo('maintenance mode disabled.')
