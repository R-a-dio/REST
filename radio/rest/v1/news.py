from radio.core.cursor import Cursor

from . import app
from ..app import API

@app.path("/news/list/(\d+)")
class listing(object):

    __metaclass__ = API

    def GET(self, limit):
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
            ret = []
            for id, header, time in cur:
                ret.append({
                    'id': id,
                    'title': header,
                    'post_time': time,
                })
            return ret

    def DELETE(id):
        pass

    def PUT(id):
        pass

    def POST(id):
        pass

@app.path("/news/(\d+)")
class detail(object):

    __metaclass__ = API

    def GET(self, nid):
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
