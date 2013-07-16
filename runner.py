from __future__ import unicode_literals
from __future__ import absolute_import

import web
import radio.core


RUNNING = True

from radio.rest import app


if __name__ == "__main__":
    radio.core.load("radio.conf.yaml")
    # Import all the APIs we have here.
    from radio.rest import v1

    application = web.application(app.get_urls(), app.get_classes(), False)
    application.run()
