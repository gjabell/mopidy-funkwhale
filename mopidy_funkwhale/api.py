import logging
import requests

import models
from uri import get_id

logger = logging.getLogger(__name__)


class FunkwhaleApi:
    def __init__(self, host, session):
        self.host = host
        self.user = user
        self.password = password
        self.session = session

    def _get_request(self, path):
        try:
            res = self.session.get(path)
        except Exception as e:
            logger.warning('FunkwhaleApi request failed for %s: %s' % (path, str(e)))
            return None

        if not res.ok:
            logger.warning('FunkwhaleApi request for %s returned status code %d' % (path, res.status_code))
            return None
        return res.json()

    def _get_playlists(self):
        json = self._get_request('%s/api/v1/playlists' % self.host)
        if not json:
            return []
        playlists = json['results']
        if not playlists:
            logger.warning('Funkwhale library has no playlists.')
            return []
        return playlists

    def _get_playlist(self, uri):
        playlist = self._get_request('%s/api/v1/playlists/%s' % (self.host, get_id(uri)))
        if not playlist:
            logger.warning('Funkwhale playlist is empty.')
            return None
        return playlist

    def _get_playlist_tracks(self, uri):
        json = self._get_request('%s/api/v1/playlists/%s/tracks' % (self.host, get_id(uri)))
        if not json:
            return []
        items = json['results']
        if items is None:
            logger.warning('Funkwhale playlist has no tracks.')
            return []
        return [i for i in map(lambda t: t['track'], items)]

    def _get_track(self, uri):
        json = self._get_request('%s/api/v1/tracks/%s' % (self.host, get_id(uri)))
        if not json:
            logger.warning('Funkwhale track is invalid')
            return None
        return json

    def _get_playback(self, uri):
        track = self._get_track(uri)
        if not track:
            return None
        return '%s/%s' % (self.host, track['listen_url'])

    def get_playlists_refs(self):
        return [models.playlist_ref(playlist) for playlist in self._get_playlists()]

    def get_playlist_ref(self, uri):
        return models.playlist_ref(self._get_playlist(uri))

    def get_playlist(self, uri):
        return models.playlist(self._get_playlist(uri), self._get_playlist_tracks(uri))

    def get_playlist_items_refs(self, uri):
        return [models.track_ref(track) for track in self._get_playlist_tracks(uri)]

    def get_playlist_items(self, uri):
        return [models.track(track) for track in self._get_playlist_tracks(uri)]

    def get_track(self, uri):
        return models.track(self._get_track(uri))

    def get_tracks(self, uris):  # TODO might be a better endpoing for multiple tracks
        return [models.track(track) for track in [self._get_track(uri) for uri in uris]]

    def get_playback(self, uri):
        return self._get_playback(uri)
