from __future__ import unicode_literals
from __future__ import absolute_import

import web
import radio.core


RUNNING = True

from . import app


if __name__ == "__main__":
    radio.core.load("radio.conf.yaml")

    # Import all the APIs we have here.
    from . import v1

    application = web.application(app.get_urls(), app.get_classes(), False)
    application.run()
