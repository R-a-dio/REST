from radio.core.cursor import Cursor

from . import app
from ..app import API

class detail(object):
    __metaclass__ = API

    def GET(self, user_id):
        with Cursor() as cur:
            if user_id is not None:
                count = cur.execute("""
                SELECT id, user, djid, privileges
                FROM users
                WHERE id=%s
                LIMIT 1
                """, (user_id,))

                if count == 0:
                    return {"errno": 1, "error": "user does not exist."}
            else:
                cur.execute("""
                SELECT id, user, djid, privileges
                FROM users
                LIMIT 50
                """)
            ret = []
            for id, user, djid, privileges, in cur:
                ret.append({
                    'id': id,
                    'name': user,
                    'dj_id': -1 if not djid else djid,
                    'permissions': privileges,
                    # New-style permissions
                    #'permissions' {
                    #    'accept': p_accept,  # accept pending songs
                    #    'delete': p_delete, # database delete access
                    #    'read': p_read, # database read access
                    #    'edit': p_edit, # database update access
                    #    'dj': p_dj, # able to use DJ proxy login
                    #    'news': p_news, # able to post/edit news
                    #    'admin': p_admin, # full admin console access (users)
                    #    'dev': p_dev, # experimental console access (alerts, maintenance, relays)
                    #},
                })
            return ret
