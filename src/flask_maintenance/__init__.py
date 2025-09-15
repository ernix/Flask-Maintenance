import os
from flask import (
    abort,
    current_app,
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
        if request.endpoint != 'static':
            _path = self.lock_filepath()
            if os.path.exists(_path) and os.path.isfile(_path):
                abort(503)
