from __future__ import unicode_literals
from __future__ import absolute_import
from functools import wraps
import json

import web


class API(type):
    """
    Metaclass that modifies the class to either be a REST API entry point
    or an python accessable API.
    """
    def __new__(meta, name, bases, dct):
        import __main__
        if hasattr(__main__, "RUNNING"):
            for key in ("GET", "POST", "DELETE", "PUT"):
                if key not in dct:
                    continue
                dct[key] = encode(dct[key])

        return super(API, meta).__new__(meta, name, bases, dct)


class App(object):
    global_classes = {}

    def __init__(self, version):
        super(App, self).__init__()
        self.version = version
        self.classes = {}

    def path(self, path):
        """
        Decorator for classes in use with web.py, with this you can do
        the following and the class will properly be registered with
        web.py on startup.

        ```python
        @path("/")
        class klass(API):
            pass
        ```
        """
        if path.startswith("/"):
            path = "/" + self.version + path + "[/]?"
        else:
            path = "/" + self.version + "/" + path + "[/]?"

        print path
        def wrapper(kls):
            name = '%s.%s' % (kls.__module__, kls.__name__)

            self.classes[name] = (path, kls)
            self.global_classes[name] = (path, kls)            # Update our global maps

            return kls

        return wrapper


def get_urls():
    urls = []
    for name, value in App.global_classes.iteritems():
        urls.append(value[0])
        urls.append(name)

    return urls

def get_classes():
    classes = {}
    for name, value in App.global_classes.iteritems():
        classes[name] = value[1]

    return classes

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


#@path("/schema/")
class schema(object):
    @encode
    def GET(self):
        uris = dict(zip(urls[1::2], urls[::2]))

        schema = {}
        for name in names:
            schema[uris[name]] = name

        return schema
