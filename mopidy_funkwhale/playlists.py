import logging

from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhalePlaylistsProvider(backend.PlaylistsProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaylistsProvider, self).__init__(*args, **kwargs)
        self.client = self.backend.client
        self.verbose = self.backend.verbose
        self.playlists = []

    def as_list(self):
        if self.verbose:
            logger.warning('%s as_list called' % __name__)
        if len(self.playlists) == 0:
            self.refresh()
        return self.playlists

    def create(self, name):
        if self.verbose:
            logger.warning('%s create called' % __name__)
        playlist = self.client.create_playlist(name)
        self.refresh()
        return playlist

    def delete(self, uri):
        if self.verbose:
            logger.warning('%s delete called' % __name__)
        success = self.client.delete_playlist(uri=uri)
        self.refresh()
        return success

    def get_items(self, uri):
        if self.verbose:
            logger.warning('%s get_items called' % __name__)
        return self.client.get_playlist_items_refs(uri=uri)

    def lookup(self, uri):
        if self.verbose:
            logger.warning('%s lookup called' % __name__)
        return self.client.get_playlist(uri=uri)

    def refresh(self):
        if self.verbose:
            logger.warning('%s refresh called' % __name__)
        self.playlists = self.client.get_playlists_refs()

    def save(self, playlist):
        if self.verbose:
            logger.warning('%s save called' % __name__)
        return self.client.save_playlist(playlist)
