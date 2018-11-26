import logging
logger = logging.getLogger(__name__)


class FunkwhaleApi():
    def __init__(self):
        pass

    def get_playlists(self):
        try:
            response = requests.get(, auth=(,))
        except Exception as e:
            logger.warning('FunkwhaleApi get_playlists request failed: %s' % str(e))
            return []
        if response.status_code != 200:
            logger.warning('FunkwhaleApi get_playlists request returned non-200 status code: %d' % response.status_code)
            return []
        playlists = response.json()['results']
        if playlists is None:
            logger.warning('Funkwhale library has no playlists.')
            return []
        return playlists
