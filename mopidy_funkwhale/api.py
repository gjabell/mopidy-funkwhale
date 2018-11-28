import requests
from mopidy.models import Playlist, Ref
from datetime import datetime

import logging
logger = logging.getLogger(__name__)


class FunkwhaleApi():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def _get_request(self, path):
        try:
            res = requests.get(path, auth=(self.user, self.password))
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
        playlist = self._get_request('%s/api/v1/playlists/%s' % (self.host, uri))
        if not playlist:
            logger.warning('Funkwhale playlist is empty.')
            return None
        return playlist

    def _get_playlist_tracks(self, uri):
        json = self._get_request('%s/api/v1/playlists/%s/tracks' % (self.host, uri))
        if not json:
            return []
        items = json['results']
        if items is None:
            logger.warning('Funkwhale playlist has no tracks.')
            return []
        return items

    def get_playlists_refs(self):
        return [models.playlist_ref(playlist) for playlist in self._get_playlists()]

    def get_playlist_ref(self, uri):
        return models.playlist_ref(self._get_playlist(uri))

    def get_playlist(self, uri):
        return models.playlist(self._get_playlist(uri), self._get_playlist_tracks(uri))

    def get_playlist_items(self, uri):
        return [_track_to_ref(track) for track in self._get_playlist_tracks(uri)]

    def get_playlist_tracks(self, uri):
        return [_track_to_track(track) for track in self._get_playlist_tracks(uri)]

