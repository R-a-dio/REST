import web
import json

from radio.core.cursor import Cursor
from .api import encode, path, error

@path("/queue/(\d+)[/]?")
class queue(object):
    @encode
    def GET(self, limit):
        """
        GET /queue[/<limit, int>/]

        Returns the next <limit> songs in the queue.
        """
        if int(limit) > 25:
            return error("Requested queue too large")
        with Cursor() as cur:
            cur.execute("""
                SELECT meta,
                       UNIX_TIMESTAMP(time) AS timestr,
                       type,
                       trackid,
                       length
                FROM queue
                ORDER BY timestr ASC
                LIMIT {:d}
            """.format(int(limit)))
            ret = []
            for meta, timestr, type, trackid, length in cur:
                ret.append({
                    'id': trackid, # Internal song ID. 0 if not an AFK song.
                    'track': meta, # Song metadata
                    'time': timestr, # ETA for song playing
                    'length': length, # length in seconds.
                    'type': type # internal
                })
            return ret
