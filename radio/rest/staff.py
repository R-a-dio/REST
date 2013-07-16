import web
import json
from radio.core.cursor import Cursor
from .api import path, encode, error

@path("/staff/(\d+)/")
class detail(object):
    @encode
    def GET(self, djid):
        with Cursor() as cur:
            count = cur.execute("""
                SELECT id, djname, djtext, djimage, djcolor
                FROM djs
                WHERE visible='1' AND id=%s
            """, (djid,))

            if count == 0:
                return error("Dj ID does not exist.")
            for id, name, text, image, color in cur:
                colors = color.split(" ")
                ret = {
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
                }
            return ret


@path("/staff/")
class listing(object):
    @encode
    def GET(self):
        with Cursor() as cur:
            cur.execute("""
                SELECT id, djname, djimage, djcolor
                FROM djs
                WHERE visible='1'
                ORDER BY priority ASC
            """)

            ret = []
            for id, name, image, color in cur:
                ret.append({
                    'id': id,
                    'name': name,
                    'image': image,
                    'color': color,
                })
            return ret
