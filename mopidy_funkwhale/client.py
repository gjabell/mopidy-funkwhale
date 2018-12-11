import models

import translator


def convert_uri(fn):
    def _wrapper(*args, **kwargs):
        for k, v in kwargs.iteritems():
            if k is 'uri':
                kwargs[k] = translator.get_id(v)
            elif k is 'uris':
                kwargs[k] = [translator.get_id(u) for u in v]
        return fn(*args, **kwargs)

    return _wrapper


class FunkwhaleClient:
    def __init__(self, api):
        self.api = api

    def get_playlists_refs(self):
        return [models.playlist_ref(p) for p in
                self.api.load_all(self.api.get_playlists())]

    @convert_uri
    def get_playlist_ref(self, uri=None):
        return models.playlist_ref(self.api.get_playlist(uri))

    @convert_uri
    def get_playlist(self, uri=None):
        return models.playlist(self.api.get_playlist(uri),
                               self.api.get_playlist_tracks(uri))

    @convert_uri
    def get_playlist_items_refs(self, uri=None):
        return [models.track_ref(t) for t in self.api.get_playlist_tracks(uri)]

    @convert_uri
    def get_playlist_items(self, uri=None):
        return [models.track(t) for t in self.api.get_playlist_tracks(uri)]

    @convert_uri
    def get_track(self, uri=None):
        return models.track(self.api.get_track(uri))

    @convert_uri
    def get_tracks_list(self, uris=None):
        # TODO might be a better endpoint for multiple tracks
        return [models.track(t) for t in [self.api.get_track(u) for u in uris]]

    @convert_uri
    def get_playback(self, uri=None):
        return self.api.get_playback(uri)
