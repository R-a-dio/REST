import web

from radio.core.cursor import Cursor
from .api import encode, path, error

@path("/relays[/]?")
class relay_list(object):
    @encode
    def GET(self):
        """
        GET /relays[/]

        Returns a listing of all relays.
        """
        with Cursor() as cur:
            cur.execute("""
                SELECT id,
                       relay_name,
                       port,
                       mount,
                       bitrate,
                       format,
                       priority,
                       active,
                       listeners,
                       listener_limit,
                       country,
                       disabled
                FROM relays
                ORDER BY id ASC
            """)
            ret = []
            for id, relay_name, port, mount, bitrate, format, \
                priority, active, listeners, listener_limit, \
                country, disabled  in cur:
                ret.append({
                    'id': id, # Internal Database ID
                    'name': relay_name,
                    'port': port,
                    'mount': mount,
                    'bitrate': bitrate,
                    'format': format,
                    'priority': priority,
                    'active': active,
                    'listeners': listeners,
                    'limit': listener_limit,
                    'country_code': country,
                    'disabled': disabled,
                })
            if not ret:
                return error("no relays available. contact a dev.")
            return ret        
