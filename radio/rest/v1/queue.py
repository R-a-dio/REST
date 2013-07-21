from radio.core.cursor import Cursor
from flask import request

from . import app
from ..app import API

class Queue(object):
    __metaclass__ = API

    @app.get("/queue/")
    def peek_top(self):
        limit = request.args.get('limit', 5)
        offset = request.args.get('offset', 0)
        return self.iter(limit, offset)

    def iter(self, limit, offset):
        """
        GET /queue[/[?limit=<int:limit>[&offset=<int:offset>]]]

        Returns the next <limit> songs in the queue,
        with <offset> from the start for pagination.
        TODO: metadata on JSON to return the next/previous URL

        `"metadata" : { "next" : <url> }`
        """
        if not limit:
            limit = 5
        elif int(limit) > 25:
            return {"error": "request too large"}
        if not offset:
            offset = 0
        with Cursor() as cur:
            count = cur.execute("""
                SELECT meta,
                       UNIX_TIMESTAMP(time) AS timestr,
                       type,
                       trackid,
                       length
                FROM queue
                ORDER BY timestr ASC
                LIMIT %s, %s
            """, (int(offset), int(limit)))

            if not count:
                return {"error": "no queue available"}

            res = {'queue': []}
            queue = res['queue']
            for meta, timestr, type, trackid, length in cur:
                queue.append({
                    'id': trackid, # Internal song ID. 0 if not an AFK song.
                    'track': meta, # Song metadata
                    'time': timestr, # ETA for song playing
                    'length': length, # length in seconds.
                    'type': type # internal
                })

            return res
