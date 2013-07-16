from __future__ import unicode_literals
from __future__ import absolute_import

import web
import radio.core

from radio.rest import fave, news, queue, relay, song, comment, account, staff
from radio.rest import api


if __name__ == "__main__":
    radio.core.load("radio.conf.yaml")

    app = web.application(radio.rest.api.urls, radio.rest.api.names, False)
    app.run()
