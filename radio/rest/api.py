from __future__ import unicode_literals
from __future__ import absolute_import
from functools import wraps
import json

import web

urls = []
names = {}


def path(path):
    """
    Decorator for classes in use with web.py, with this you can do
    the following and the class will properly be registered with
    web.py on startup.

    ```python
    @path("/")
    class klass:
        pass
    ```
    """
    def wrapper(kls):
        name = '%s.%s' % (kls.__module__, kls.__name__)

        # Add ourself to the url list
        urls.extend([path, name])
        # Add ourself to the class dict
        names[name] = kls

        return kls
    return wrapper


defaults = ("json",)


def encode(accepted=defaults):
    def wrapper(func):
        @wraps(func)
        def caller(*args, **kwargs):
            res = func(*args, **kwargs)

            web.header('Content-Type', 'application/json')

            return json.dumps(
                res,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

        return caller
    return wrapper(accepted) if callable(accepted) else wrapper


def error(message):
    return {"error": message}


def normalize(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


urls_old = (
    "/users/(all)/",       "account",
    "/staff/(\d+)/",       "staff_detail",
    "/staff/list/",        "staff_list",
    #    "/users/(\w+)/faves/", "fave",
    "/users/(\w+)/",       "account",
    "/relays/(\w+/|$)",    "relay",
    "/songs/queue/"        "queue",
    "/songs/(all)/",       "song",
    "/comments/(\d+)/",    "comment",
    "/news/(\d+)/",        "news"
    "/(.*)",               "index",
)
