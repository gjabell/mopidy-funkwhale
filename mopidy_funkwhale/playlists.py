from mopidy import backend

import logging
logger = logging.getLogger(__name__)

class FunkwhalePlaylistProvider(backend.PlaylistProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaylistProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api
        self.playlists = []
        self.refresh()


    def as_list(self):
        return self.api.get_playlists()

    def create(self, name):
        pass

    def delete(self, uri):
        pass

    def get_items(self, uri):
        pass

    def lookup(self, uri):
        pass

    def refresh(self):
        pass

    def save(self, playlist):
        pass

