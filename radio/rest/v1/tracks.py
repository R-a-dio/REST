from radio.core.cursor import Cursor
from radio.core.requests import requestable

from . import app
from ..app import API

class Track(object):
    __metaclass__ = API

    @app.get("/tracks/<int:id>/")
    def get(self, id):
        #print song_id
        with Cursor() as cur:
            count = cur.execute("""
                SELECT id, artist, track, album, tags, priority,
                       UNIX_TIMESTAMP(lastplayed) as lp,
                       UNIX_TIMESTAMP(lastrequested) as lr,
                       accepter, lasteditor,
                       requestcount, usable
                FROM tracks
                WHERE id=%s
                LIMIT 1
                """, (id,))

            if count == 0:
                return {"error": "song does not exist."}
            return self.from_cursor(cur)

    @app.get("/tracks/latest/")
    def latest_additions(self):
        with Cursor() as cur:
            cur.execute("""
                SELECT id, artist, track, album, tags, priority,
                       UNIX_TIMESTAMP(lastplayed) as lp,
                       UNIX_TIMESTAMP(lastrequested) as lr,
                       accepter, lasteditor,
                       requestcount, usable
                FROM tracks
                ORDER BY id DESC
                LIMIT 10 -- latest 10 songs
                """)

            return self.from_cursor(cur)

    def from_cursor(self, cursor):
        res = {"tracks": []}
        tracks = res['tracks']
        for (id, artist, track, album, tags, priority, lp, lr,
                accepter, lasteditor, requestcount, usable) in cursor:

            track = {
                'id': id,
                'last_played': lp,
                'last_requested': lr,
                'requestable': requestable(usable, requestcount, lp, lr),
                'metadata': {
                    # Complete lack of error-handling here
                    'artist': artist,
                    'track': track,
                    'album': album,
                    'tags': tags,
                },
                'accepter': accepter,
            }

            tracks.append(track)
        return res

