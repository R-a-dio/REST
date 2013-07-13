import web
import json
from radio.core.cursor import Cursor
from .api import path, encode


@path("/faves/(\w+)/")
class fave(object):
    @encode
    def GET(self, name):
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

    def DELETE(id):
        pass

    def PUT(id):
        pass

    def POST(id):
        pass
