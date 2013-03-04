import web
from index import *
from account, relay import *
from song, fave, queue import *
from news, comment import *

urls = (
    "/users/(all)/",       "account",
    "/users/(\w+)/faves/", "fave",
    "/users/(\w+)/",       "account",
    "/relays/(\w+|$)/",    "relay",
    "/songs/queue/"        "queue",
    "/songs/(all)/",       "song",
    "/comments/(\d+)/",    "comment",
    "/news/(\d+)/",        "news"
    "/(.*)",               "index",
)

class index:
    def GET(url):
        pass
    
class account:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass

class fave:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass

class relay:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass

class queue:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass
    
class song:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass
    
class comment:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass
    
class news:
    def GET(id):
        pass
    
    def DELETE(id):
        pass
    
    def PUT(id):
        pass
    
    def POST(id):
        pass
    