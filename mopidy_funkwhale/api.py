import time

import logging

import models
from uri import get_id, get_track_uri

logger = logging.getLogger(__name__)


class Cache(object):
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, func):
        def _memoized(*args):
            self.func = func
            now = time.time()
            try:
                value, last_update = self.cache[args]
                age = now - last_update
                if age > self.ttl:
                    raise AttributeError

                return value

            except (KeyError, AttributeError):
                value = self.func(*args)
                self.cache[args] = (value, now)
                return value

            except TypeError:
                return self.func(*args)

        return _memoized


class FunkwhaleApi:
    def __init__(self, host, session):
        self.host = host
        self.session = session

    def _get_request(self, path):
        try:
            r = self.session.get(path)
        except Exception as e:
            logger.warning('FunkwhaleApi request failed for %s: %s' % (path, str(e)))
            return None

        if not r.ok:
            logger.warning('FunkwhaleApi request for %s returned status code %d' % (path, r.status_code))
            return None
        return r.json()

    def _post_request(self, path, body=None):
        body = body or {}
        try:
            r = self.session.post(path, data=body)
        except Exception as e:
            logger.warning('FunkwhaleApi request failed for %s: %s' % (path, str(e)))
            return None

        if not r.ok:
            logger.warning('FunkwhaleApi request for %s returned status code %d' % (path, r.status_code))
            return None
        return r.json()

    @Cache()
    def _get_playlists(self):
        json = self._get_request('%s/api/v1/playlists' % self.host)
        if not json:
            return []
        playlists = json['results']
        if not playlists:
            logger.warning('Funkwhale library has no playlists.')
            return []
        return playlists

    @Cache()
    def _get_tracks(self):
        url = '%s/api/v1/tracks' % self.host
        tracks = []
        while url:
            json = self._get_request(url)
            if not json:
                return tracks
            results = json['results']
            if not results:
                return tracks
            tracks += [self._get_track(uri) for uri in [get_track_uri(t) for t in results]]
            url = json['next']
            if not url:
                return tracks
        return tracks

    @Cache()
    def _get_playlist(self, uri):
        playlist = self._get_request('%s/api/v1/playlists/%s' % (self.host, get_id(uri)))
        if not playlist:
            logger.warning('Funkwhale playlist is empty.')
            return None
        return playlist

    @Cache()
    def _get_playlist_tracks(self, uri):
        json = self._get_request('%s/api/v1/playlists/%s/tracks' % (self.host, get_id(uri)))
        if not json:
            return []
        items = json['results']
        if items is None:
            logger.warning('Funkwhale playlist has no tracks.')
            return []
        return [self._get_track(uri) for uri in [get_track_uri(i['id']) for i in map(lambda t: t['track'], items)]]

    @Cache()
    def _get_track(self, uri):
        json = self._get_request('%s/api/v1/tracks/%s' % (self.host, get_id(uri)))
        if not json:
            logger.warning('Funkwhale track is invalid')
            return None
        return json

    @Cache()
    def _get_token(self):
        json = self._post_request('%s/api/v1/token/' % self.host,
                                  {'username': self.session.auth[0], 'password': self.session.auth[1]})
        if not json:
            logger.warning('Funkwhale failed to get token')
            return None
        token = json['token']
        if not token:
            logger.warning('Funkwhale returned invalid token')
            return None
        return token

    @Cache()
    def _get_playback(self, uri):
        track = self._get_track(uri)
        token = self._get_token()
        if not track:
            return None
        return '%s%s?jwt=%s' % (self.host, track['listen_url'], token)

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

    def get_tracks_list(self, uris):  # TODO might be a better endpoing for multiple tracks
        return [models.track(track) for track in [self._get_track(uri) for uri in uris]]

    def get_tracks(self):
        return self._get_tracks()

    def get_playback(self, uri):
        return self._get_playback(uri)
