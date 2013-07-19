from __future__ import unicode_literals
from __future__ import absolute_import
from functools import wraps, partial
from collections import defaultdict
import json
import inspect

from flask import request, make_response
from method_decorator import method_decorator


class PartialInstance(object):
    def __init__(self, func):
        super(PartialInstance, self).__init__()
        self.func = func
        self.kls = None

    def __call__(self, *args, **kwargs):
        if self.kls is None:
            return self.func(*args, **kwargs)
        return self.func(self.kls(), *args, **kwargs)


class API(type):
    """
    Metaclass that modifies the class to either be a REST API entry point
    or an python accessable API.
    """
    def __new__(meta, name, bases, dct):
        import __main__
        if hasattr(__main__, "RUNNING"):
            for name, func in dct.items():
                if getattr(func, "marked", False):
                    route, methods = func.route, func.methods

                    func = encode(func)
                    func.is_method = True

                    func = PartialInstance(func)

                    for method in methods:
                        route.add_method(method, func)

                    dct[name] = func

        kls = super(API, meta).__new__(meta, name, bases, dct)

        for func in dct.values():
            if isinstance(func, PartialInstance):
                func.kls = kls

        return kls


class Route(object):
    """
    A simple route class that will call a specific function dependant
    on the `request.method` value on call.

    Registering of methods can be done with :meth:`add_method`.
    """
    def __init__(self, path):
        super(Route, self).__init__()

        self.path = self.__name__ = path
        self.methods = {}

    def add_method(self, method, function):
        """
        Register `function` for `method` on this :class:`Route`.
        """
        self.methods[method.upper()] = function

    def __call__(self, *args, **kwargs):
        method = request.method.upper()

        func = self.methods.get(method)

        if getattr(func, "is_method", False):
            return func(None, *args, **kwargs)
        else:
            return func(*args, **kwargs)
        return error("Method not supported", 404)


class App(object):
    routes = {}

    def __init__(self, version):
        super(App, self).__init__()
        self.version = version

    def route(self, path, methods):
        """
        Decorator for classes in use with web.py, with this you can do
        the following and the class will properly be registered with
        web.py on startup.

        ```python
        @app.route("/", ['GET'])
        class klass(API):
            pass
        ```
        """
        if path.startswith("/"):
            path = "/" + self.version + path
        else:
            path = "/" + self.version + "/" + path

        try:
            route = self.routes[path]
        except KeyError:
            route = Route(path)
            self.routes[path] = route

        print path, methods

        def wrapper(func):
            # Mark and add some bookkeeping for later
            # We can't register it here yet since the API metaclass
            # hasn't had a chance to touch the function yet.
            func.marked = True
            func.methods = methods
            func.route = route

            return func

        return wrapper

    def __getattr__(self, key):
        return partial(self.route, methods=[key])

    @classmethod
    def register_routes(cls, app):
        """
        Finalizer that should be called when all routes have been registered.

        This registers all the routes with flask.
        """
        for path, route in cls.routes.iteritems():
            app.route(path)(route)

defaults = ("json",)


def encode(accepted=defaults):
    def wrapper(func):
        @wraps(func)
        def caller(*args, **kwargs):
            res = func(*args, **kwargs)

            # If the result is not a dict we don't want to touch it
            if not isinstance(res, dict):
                return res

            json_resp = json.dumps(
                res,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )

            resp = make_response(json_resp, 200)
            resp.headers['Content-Type'] = 'application/json'

            return resp

        return caller
    return wrapper(accepted) if callable(accepted) else wrapper


def error(message, code=501):
    return encode(lambda: {"error": message})(), code



def normalize(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


class DuplicateRegistration(Exception):
    pass
