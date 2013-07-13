from __future__ import unicode_literals
from __future__ import absolute_import

import web
import radio.core

from . import fave, news, queue, relay, song, comment, account, staff
from . import api


if __name__ == "__main__":
    radio.core.load("radio.conf.yaml")

    app = web.application(api.urls, api.names, False)
    app.run()
