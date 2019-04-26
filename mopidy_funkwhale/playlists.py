import logging

from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhalePlaylistsProvider(backend.PlaylistsProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaylistsProvider, self).__init__(*args, **kwargs)
        self.client = self.backend.client
        self.playlists = []

    def as_list(self):
        if not self.playlists:
            self.refresh()
        return self.playlists

    def create(self, name):
        playlist = self.client.create_playlist(name)
        self.refresh()
        return playlist

    def delete(self, uri):
        success = self.client.delete_playlist(uri=uri) is not None
        self.refresh()
        return success

    def get_items(self, uri):
        return self.client.get_playlist_items_refs(uri=uri)

    def lookup(self, uri):
        return self.client.get_playlist(uri=uri)

    def refresh(self):
        self.playlists = self.client.get_playlists_refs()

    def save(self, playlist):
        return self.client.save_playlist(playlist)
