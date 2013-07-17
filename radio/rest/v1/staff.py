from radio.core.cursor import Cursor

from . import app
from ..app import API

@app.path("/staff/(\d+)?")
class detail(object):

    __metaclass__ = API

    def GET(self, djid):
        print djid
        ret = []
        with Cursor() as cur:
            if djid is not None:
                count = cur.execute("""
                SELECT id, djname, djtext, djimage, djcolor
                FROM djs
                WHERE visible='1' AND id=%s
                """, (djid,))
                
                if count == 0:
                    return {"error": "dj id does not exist."}
            else:
                cur.execute("""
                SELECT id, djname, djtext, djimage, djcolor
                FROM djs
                WHERE visible='1'
                """)
            for id, name, text, image, color in cur:
                colors = color.split(" ")
                ret.append({
                    'id': id,
                    'name': name,
                    'text': text,
                    'image': image,
                    'color': {
                        # Complete lack of error-handling here
                        'red' : colors[0],
                        'green' : colors[1],
                        'blue' : colors[2],
                    },
                })
            return ret
