import web
from index import *
from account, relay import *
from song, fave, queue import *
from news, comment import *

urls = (
    "/users/(all)/",       "account",
    "/users/(\w+)/faves/", "fave",
    "/users/(\w+)/",       "account",
    "/relays/(\w+/|$)",    "relay",
    "/songs/queue/"        "queue",
    "/songs/(all)/",       "song",
    "/comments/(\d+)/",    "comment",
    "/news/(\d+)/",        "news"
    "/(.*)",               "index",
)

    