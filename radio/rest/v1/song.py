from radio.core.cursor import Cursor

from . import app
from ..app import API

@app.path("/song[/]?(\d+)?")
class detail(object):

    __metaclass__ = API

    def GET(self, song_id):
        #print song_id
        with Cursor() as cur:
            if song_id is not None:
                count = cur.execute("""
                SELECT id,
                       artist, track, album, tags,
                       priority,
                       UNIX_TIMESTAMP(lastplayed) as lp,
                       UNIX_TIMESTAMP(lastrequested) as lr,
                       accepter, lasteditor,
                       requestcount, usable
                FROM tracks
                WHERE id=%s
                LIMIT 1
                """, (song_id,))

                if count == 0:
                    return {"error": "song does not exist."}
            else:
                cur.execute("""
                SELECT id,
                       artist, track, album, tags,
                       priority,
                       UNIX_TIMESTAMP(lastplayed) as lp,
                       UNIX_TIMESTAMP(lastrequested) as lr,
                       accepter, lasteditor,
                       requestcount, usable
                FROM tracks
                ORDER BY id DESC
                LIMIT 10 -- latest 10 songs
                """)
            ret = []
            for id, artist, track, album, tags, priority, lp, lr, \
                accepter, lasteditor, requestcount, usable in cur:
                ret.append({
                    'id': id,
                    'play_data': {
                        'last_played': lp,
                        'last_requested': lr,
                        'request_count': requestcount,
                        'priority': priority,
                    },
                    #'hash': hash,  # include this only if authed?
                    #'path': path,  # as above
                    'metadata': {
                        # Complete lack of error-handling here
                        'artist': artist,
                        'track': track,
                        'album': album,
                        'tags': tags,
                    },
                    'usable': usable,
                    'accepter': accepter,
                    'last_editor': lasteditor,
                })
            return ret

