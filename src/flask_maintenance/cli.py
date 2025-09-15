import os
import click
from flask import current_app
from flask.cli import with_appcontext


@click.group()
def maintenance():
    """Enable or disable Maintenance mode."""
    pass


@maintenance.command()
@with_appcontext
def enable():
    """
    Enable Maintenance mode.
    """
    result = False
    _path = current_app.extensions['maintenance'].lock_filepath()
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    try:
        open(_path, 'w').close()
        result = True
    except Exception as e:  # pragma: no cover
        click.echo(e)

    if result:
        click.echo('maintenance mode enabled.')
        return True

    return False  # pragma: no cover


@maintenance.command()
@with_appcontext
def disable():
    """
    Disable Maintenance mode.
    """
    _path = current_app.extensions['maintenance'].lock_filepath()
    if os.path.exists(_path) and os.path.isfile(_path):
        try:
            os.remove(_path)
        except Exception as e:  # pragma: no cover
            click.echo(e)
            return False

    click.echo('maintenance mode disabled.')
