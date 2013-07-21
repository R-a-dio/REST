from radio.core.cursor import Cursor

from . import app
from ..app import API

class Users(object):
    __metaclass__ = API

    @app.get("/users/<int:user_id>/")
    def get_user(self, user_id):
        with Cursor() as cur:
            count = cur.execute("""
                SELECT
                    u.id, u.user, u.djid,
                    p.accept, p.delete, p.read,
                    p.edit, p.dj, p.news,
                    p.admin, p.dev
                FROM
                    users as u
                JOIN
                    permissions as p
                ON
                    u.id = p.id
                WHERE u.id=%s
                LIMIT 1
                """, (user_id,))

            if count == 0:
                return {"errno": 1, "error": "user does not exist."}

            for id, user, djid, \
                p_accept, p_delete, p_read, p_edit, p_dj, p_news, \
                p_admin, p_dev in cur:
                ret = {
                    'id': id,
                    'name': user,
                    'dj_id': -1 if not djid else djid,
                    #'permissions': privileges,
                    # New-style permissions
                    'permissions': {
                        'accept': bool(p_accept),  # accept pending songs
                        'delete': bool(p_delete), # database delete access
                        'read': bool(p_read), # database read access
                        'edit': bool(p_edit), # database update access
                        'dj': bool(p_dj), # able to use DJ proxy login
                        'news': bool(p_news), # able to post/edit news
                        'admin': bool(p_admin), # full admin console access (users)
                        'dev': bool(p_dev), # experimental console access (alerts, maintenance, relays)
                    },
                }
            return {"user" : ret}

    @app.get("/users/")
    def get_all_users(self):
        with Cursor() as cur:
            cur.execute("""
                SELECT
                    u.id, u.user, u.djid,
                    p.accept, p.delete, p.read,
                    p.edit, p.dj, p.news,
                    p.admin, p.dev
                FROM
                    users as u
                JOIN
                    permissions as p
                ON
                    u.id = p.id
                LIMIT 50
                """)
            ret = []
            for id, user, djid, \
                p_accept, p_delete, p_read, p_edit, p_dj, p_news, \
                p_admin, p_dev in cur:
                ret.append({
                    'id': id,
                    'name': user,
                    'dj_id': -1 if not djid else djid,
                    #'permissions': privileges,
                    # New-style permissions
                    'permissions': {
                        'accept': bool(p_accept),  # accept pending songs
                        'delete': bool(p_delete), # database delete access
                        'read': bool(p_read), # database read access
                        'edit': bool(p_edit), # database update access
                        'dj': bool(p_dj), # able to use DJ proxy login
                        'news': bool(p_news), # able to post/edit news
                        'admin': bool(p_admin), # full admin console access (users)
                        'dev': bool(p_dev), # experimental console access (alerts, maintenance, relays)
                    },
                })
            return {"users" : ret}

