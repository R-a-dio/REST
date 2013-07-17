from __future__ import absolute_import

from ..app import App

app = App('v1')


from . import fave, queue, relay, staff, news, song
