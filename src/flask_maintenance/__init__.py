import json
import os
import sys
from typing import Optional, TypedDict

from flask import Flask, abort, current_app, redirect, request
from flask.typing import ResponseReturnValue

if sys.version_info < (3, 11):  # pragma: no cover
    from typing_extensions import NotRequired, Unpack
else:  # pragma: no cover
    from typing import NotRequired, Unpack

DEFAULT_LOCK_FILENAME = "under_maintenance"


__all__ = ["Maintenance"]


class InitOpts(TypedDict):
    lock_filename: NotRequired[str]


class Maintenance:
    """
    Add Maintenance mode feature to your flask application.
    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        **kwargs: Unpack[InitOpts],
    ) -> None:
        """
        :param app:
            Flask application object.
        """

        self.app = app

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(
        self,
        app: Flask,
        lock_filename: str = DEFAULT_LOCK_FILENAME,
    ) -> None:
        """
        Initalizes the application with the extension.

        :param app:
            Flask application object.
        """

        self.lock_filename = lock_filename
        app.before_request(self._handler)

        # register extension with app
        app.extensions = getattr(app, "extensions", {})
        app.extensions["maintenance"] = self

    def lock_filepath(self) -> str:
        return os.path.join(current_app.instance_path, self.lock_filename)

    def _handler(self) -> Optional[ResponseReturnValue]:
        """
        Maintenance mode handler.
        """
        ep = request.endpoint
        if ep is not None and ep.split(".")[-1] == "static":
            return None

        _path = self.lock_filepath()
        try:
            with open(_path, "r") as fp:
                options = json.load(fp)

            dst = options.get("redirect")
            if dst is not None:
                return redirect(dst)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:  # pragma: no cover
            pass
        except KeyError:  # pragma: no cover
            pass

        abort(503)
