import web

from .api import path


@path("/")
class index(object):
    def GET(self):
        """
        GET /
        
        Redirects to the main site. In future, this will redirect
        to the documentation.
        """
        
        raise web.seeother("https://www.r-a-d.io")
        
