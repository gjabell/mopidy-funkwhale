import requests
from mopidy.models import Playlist, Ref

import logging
logger = logging.getLogger(__name__)


Response = {
    'OK': 200
}


class FunkwhaleApi():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def get_playlists(self):
        try:
            response = requests.get(
                    '%s/api/v1/playlists' % self.host, auth=(self.user, self.password))
        except Exception as e:
            logger.warning('FunkwhaleApi get_playlists request failed: %s' % str(e))
            return []
        if response.status_code != Response['OK']:
            logger.warning('FunkwhaleApi get_playlists request returned non-200 status code: %d' % response.status_code)
            return []
        playlists = response.json()['results']
        if playlists is None:
            logger.warning('Funkwhale library has no playlists.')
            return []
        return playlists

    def get_playlist(self, playlist):
        try:
            response = requests.get(
                    playlist, auth=(self.user, self.password))
        except Exception as e:
            logger.warning('FunkwhaleApi get_playlist request failed: %s' % str(e))
            return None
        if response.status_code != Response['OK']:
            logger.warning('FunkwhaleApi get_playlist request returned non-200 status code: %d' % response.status_code)
            return None
        playlist = response.json()
        if playlist is None:
            logger.warning('Funkwhale playlist is empty.')
            return None
        return playlist

    def get_playlist_items(self, playlist):
        try:
            response = requests.get(
                    '%s/tracks' % playlist, auth=(self.user, self.password))
        except Exception as e:
            logger.warning('FunkwhaleApi get_playlist_items request failed: %s' % str(e))
            return []
        if response.status_code != Response['OK']:
            logger.warning('FunkwhaleApi get_playlist_items request returned non-200 status code: %d' % response.status_code)
            return []
        items = response.json()['results']
        if items is None:
            logger.warning('Funkwhale playlist has no tracks.')
            return []
        return items

    def get_playlists_refs(self):
        return [self.playlist_to_ref(playlist) for playlist in self.get_playlists()]

    def get_playlist_ref(self, uri):
        return self.playlist_to_ref(self.get_playlist(uri))

    def get_playlist_items_refs(self, uri):
        return [self.track_to_ref(track) for track in self.get_playlist_items(uri)]

    def playlist_to_ref(self, playlist):
        if playlist is None:
            return None
        return Ref.playlist(
            uri='%s/api/v1/playlists/%d' % (self.host, playlist['id']),
            name=playlist['name'])

    def track_to_ref(self, track):
        if track is None:
            return None
        return Ref.track(
            uri='%s/api/v1/tracks/%d' % (self.host, track['id']),
            name=track['title'])
