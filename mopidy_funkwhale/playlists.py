from mopidy import backend

import logging
logger = logging.getLogger(__name__)

class FunkwhalePlaylistsProvider(backend.PlaylistsProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaylistsProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api
        self.playlists = []
        self.refresh()

    def as_list(self):
        logger.warning('%s as_list called' % __name__)
        return self.playlists

    def create(self, name):
        logger.warning('%s create called' % __name__)

    def delete(self, uri):
        logger.warning('%s delete called' % __name__)

    def get_items(self, uri):
        logger.warning('%s get_items called' % __name__)
        return self.api.get_playlist_items(uri)

    def lookup(self, uri):
        logger.warning('%s lookup called' % __name__)
        return self.api.get_playlist(uri)

    def refresh(self):
        logger.warning('%s refresh called' % __name__)
        self.playlists = self.api.get_playlists()
        logger.warning(self.playlists)

    def save(self, playlist):
        logger.warning('%s save called' % __name__)

