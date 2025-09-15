import os
import json
from flask import (
    abort,
    current_app,
    redirect,
    request
)

DEFAULT_LOCK_FILENAME = 'under_maintenance'


__all__ = ['Maintenance']


class Maintenance:
    """
    Add Maintenance mode feature to your flask application.
    """

    def __init__(self, app=None, **kwargs):
        """
        :param app:
            Flask application object.
        """

        self.app = app

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, lock_filename=DEFAULT_LOCK_FILENAME):
        """
        Initalizes the application with the extension.

        :param app:
            Flask application object.
        """

        self.lock_filename = lock_filename
        app.before_request(self._handler)

        # register extension with app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['maintenance'] = self

    def lock_filepath(self):
        return os.path.join(current_app.instance_path, self.lock_filename)

    def _handler(self):
        """
        Maintenance mode handler.
        """
        # TODO: Use current_app.static_folder
        if request.endpoint == 'static':  # pragma: no cover
            return

        _path = self.lock_filepath()
        try:
            with open(_path, 'r') as fp:
                options = json.load(fp)

            dst = options.get('redirect')
            if dst is not None:
                return redirect(dst)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:  # pragma: no cover
            pass
        except KeyError: # pragma: no cover
            pass

        abort(503)
