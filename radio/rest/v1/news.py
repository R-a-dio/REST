from radio.core.cursor import Cursor

from . import app
from ..app import API, normalize


class News(object):
    __metaclass__ = API

    @app.get("/news/latest/")
    def latest(self):
        return self.list(limit=10)

    @app.get("/news/list/<int:limit>/")
    def list(self, limit):
        """
        GET /news/list/<limit, int>/

        Returns the last <limit> news posts.
        """
        with Cursor() as cur:
            cur.execute("""
                SELECT id, header, UNIX_TIMESTAMP(time) as utime
                FROM news
                ORDER BY time DESC
                LIMIT {:d}
            """.format(int(limit)))
            res = {"news": []}
            news = res['news']
            for id, header, time in cur:
                news.append({
                    'id': id,
                    'title': header,
                    'post_time': time,
                })

            return res

    @app.get("/news/<int:nid>/")
    def detail(self, nid):
        """
        GET /news/<id, int>/

        Returns the news body, metadata and comments
        for a given news ID (From listing).
        """
        with Cursor() as cur:
            count = cur.execute("""
                SELECT news.id, news.header, UNIX_TIMESTAMP(news.time),
                       news.newstext,
                       comments.id, comments.header,
                       UNIX_TIMESTAMP(comments.time), comments.text,
                       comments.login
                FROM news LEFT JOIN comments on news.id=comments.nid
                WHERE news.id=%s
                ORDER BY comments.time DESC
            """, (nid,))
            if count == 0:
                return error('News ID does not exist.')
            ret = {}
            for (nid, nheader, ntime, ntext,
                    cid, cheader, ctime, ctext, clogin) in cur:

                if not ret:
                    trunc = ntext.find('TRUNCATE')
                    ntext = ntext.replace('TRUNCATE', '')
                    ntext = normalize(ntext)

                    ret = {
                        'id': nid,
                        'title': nheader,
                        'post_time': ntime,
                        'content': ntext,
                        'truncate_at': trunc,
                        'comments': [],
                    }
                if cid is None:
                    break

                ret['comments'].append({
                    'id': cid,
                    'name': cheader,
                    'post_time': ctime,
                    'content': normalize(ctext),
                    'login_as': clogin if clogin else '',
                })
            return ret
