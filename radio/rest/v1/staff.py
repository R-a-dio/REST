from radio.core.cursor import Cursor

from . import app
from ..app import API


class Staff(object):
    __metaclass__ = API

    @app.get("/staff/")
    def list(self):
        res = {"staff": []}
        staff = res['staff']

        with Cursor() as cur:
            cur.execute("""
                SELECT id, djname, djtext, djimage, djcolor
                FROM djs
                WHERE visible='1'
            """)

            for id, name, text, image, color in cur:
                colors = color.split(" ")
                staff.append({
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
            else:
                return {"error": "No djs exist."}

            return res

    @app.get("/staff/<int:djid>/")
    def detail(self, djid):
        res = {"staff": []}
        staff = res['staff']
        with Cursor() as cur:
            count = cur.execute("""
                SELECT id, djname, djtext, djimage, djcolor
                FROM djs
                WHERE visible='1' AND id=%s
                """, (djid,))

            if count == 0:
                return {"error": "dj id does not exist."}

            for id, name, text, image, color in cur:
                colors = color.split(" ")
                return {
                    'id': id,
                    'name': name,
                    'text': text,
                    'image': image,
                    'color': {
                        'red': colors[0],
                        'green': colors[1],
                        'blue': colors[2],
                    },
                }
