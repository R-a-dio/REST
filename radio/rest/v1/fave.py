from __future__ import absolute_import
from __future__ import unicode_literals

from radio.core.cursor import Cursor

from . import app
from ..app import API


class Fave(object):
    __metaclass__ = API

    @app.get("/faves/<name>/")
    def for_nick(self, name):
        with Cursor() as cur:
            cur.execute("""
                SELECT efave.id, enick.id,
                       enick.nick, esong.id,
                       esong.meta
                FROM enick JOIN efave ON enick.id = efave.inick
                           JOIN esong ON efave.isong = esong.id
                WHERE LOWER(enick.nick) = LOWER(%s)
                """, (name,))
            ret = {
                'nick_id': 0,
                'nickname': '',
                'faves': [],
            }
            for faveid, nickid, nickname, songid, meta in cur:
                ret['nick_id'] = nickid
                ret['nickname'] = nickname
                ret['faves'].append({
                    'song_id': songid,
                    'meta': meta,
                })
            return ret
