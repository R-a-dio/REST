from __future__ import unicode_literals
from __future__ import absolute_import

import flask
import radio.core


RUNNING = True

from radio.rest import app


if __name__ == "__main__":
    radio.core.load("radio.conf.yaml")
    # Import all the APIs we have here.
    from radio.rest import v1

    # Create our application of flask
    application = flask.Flask("radio.rest")

    # Get everything to register
    app.App.register_routes(application)

    application.run(host='0.0.0.0', port=8050, debug=True)
