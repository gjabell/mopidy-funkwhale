import copy
import logging
import time
import urllib
import urlparse

from mopidy import httpclient

import requests

import mopidy_funkwhale

logger = logging.getLogger(__name__)


# Modified from https://code.eliotberriot.com/funkwhale/mopidy/
#                       blob/master/mopidy_funkwhale/client.py
class SessionWithUrlBase(requests.Session):
    def __init__(self, url_base=None):
        super(SessionWithUrlBase, self).__init__()
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        if url.startswith("http://") or url.startswith("https://"):
            modified_url = url
        else:
            modified_url = urlparse.urljoin(self.url_base, url)
        return super(SessionWithUrlBase, self).request(method, modified_url,
                                                       **kwargs)


def make_session(config):
    proxy = httpclient.format_proxy(config['proxy'])
    agent = httpclient.format_user_agent('%s/%s' % (
        mopidy_funkwhale.Extension.dist_name,
        mopidy_funkwhale.__version__))

    funkwhale_config = config['funkwhale']
    url = urlparse.urljoin(funkwhale_config['host'], '/api/v1/')

    session = SessionWithUrlBase(url_base=url)
    session.proxies.update({'http': proxy, 'https': proxy})
    session.headers.update({'user-agent': agent})

    return session


# Modified from https://code.eliotberriot.com/funkwhale/mopidy/
#                       blob/master/mopidy_funkwhale/library.py
class Cache(dict):
    def __init__(self, cache_time=3600):
        self.cache_time = cache_time
        super(Cache, self).__init__()

    def set(self, key, value):
        if not self.cache_time:
            return
        now = time.time()
        # copy the value to ensure mutation doesn't affect the cache
        cp = copy.deepcopy(value)
        self[key] = (now, cp)

    def get(self, key):
        if not self.cache_time:
            return None
        value = super(Cache, self).get(key)
        if not value:
            return None
        now = time.time()
        t, v = value
        if t + self.cache_time < now:
            del self[key]
            return None
        # copy the value to ensure mutation doesn't affect the cache
        return copy.deepcopy(v)

    def remove(self, key):
        try:
            del self[key]
        except KeyError:
            return


class FunkwhaleApi(object):
    def __init__(self, config):
        self.session = make_session(config)
        self.token = None
        self.host = config['funkwhale']['host']
        self.username = config['funkwhale']['user']
        self.password = config['funkwhale']['password']
        self.cache = Cache(config['funkwhale']['cache_time'])

    def login(self):
        json = self._post('token/', {'username': self.username,
                                     'password': self.password})
        if not json:
            return None
        token = json['token']
        self.session.headers.update({'Authorization': 'JWT %s' % token})
        self.token = token
        return token

    def _get(self, path):
        cached = self.cache.get(path)
        if cached is not None:
            return cached

        r = self.session.get(path)
        r.raise_for_status()

        if r.status_code == 204:
            return {}

        json = r.json()
        self.cache.set(path, json)
        return json or {}

    def _post(self, path, body=None):
        body = body or {}

        r = self.session.post(path, data=body)
        r.raise_for_status()

        # delete cache reference
        for key in self.cache.keys():
            if key.startswith(path):
                self.cache.remove(key)

        if r.status_code == 204:
            return {}

        return r.json() or {}

    def _delete(self, path):
        r = self.session.delete(path)
        r.raise_for_status()

        # delete cache reference
        for key in self.cache.keys():
            if key.startswith(path):
                self.cache.remove(key)

        return {}

    def get_playlists(self):
        """
        Get a paged list of playlists on the server.

        :return: A JSON list of playlists.
        """
        return self._get('playlists/')

    def get_playlist(self, id):
        """
        Get a single playlist from the server.

        :id: The Funkwhale id of the playlist.

        :return: A JSON representation of the playlist.
        """
        return self._get('playlists/%s/' % id)

    def get_playlist_tracks(self, id):
        """
        Get a single playlist's tracks from the server.

        :id: The Funkwhale id of the playlist.

        :return: A JSON list of tracks.
        """
        return self._get('playlists/%s/tracks/' % id)['results']

    def get_tracks(self):
        """
        Get a paged list of tracks on the server.

        :return: A JSON list of tracks.
        """
        return self._get('tracks/')

    def get_track(self, id):
        """
        Get a single track from the server.

        :id: The Funkwhale id of the track.

        :return: A JSON representation of the track.
        """
        return self._get('tracks/%s/' % id)

    def get_favorite_tracks(self):
        """
        Get a paged list of favorite tracks from the server.

        :return: A JSON list of tracks.
        """
        return self._get('favorites/tracks/')

    def favorite_track(self, id):
        """
        Add a track to favorites.

        :id: The Funkwhale id of the track.

        :return: A JSON representation of the favorite.
        """
        return self._post('favorites/tracks/', {'track': int(id)})

    def unfavorite_track(self, id):
        """
        Removes a track from favorites.

        :id: The Funkwhale id of the track.

        :return: An empty dictionary.
        """
        res = self._post('favorites/tracks/remove/', {'track': int(id)})

        # manually remove cache entry, since it has a different path
        self.cache.remove('favorites/tracks/')

        return res

    def get_playback(self, id):
        """
        Get the playback url for a single track.

        :id: The Funkwhale id of the track.

        :return: The playback url, including jwt token.
        """
        track = self.get_track(id)
        uploads = track['uploads']
        if not uploads:
            return None
        try:
            (scheme, host, _, _, _) = urlparse.urlsplit(self.host)
            (_, _, path, query, _) = urlparse.urlsplit(
                uploads[0]['listen_url'])
            queries = {'jwt': self.token}
            queries.update(urlparse.parse_qsl(query))
            return urlparse.urlunsplit(
                (scheme, host, path, urllib.urlencode(queries), ''))
        except KeyError:
            return None

    def create_playlist(self, name):
        """
        Create a new, empty playlist on the server.

        :name: The name of the playlist.

        :return: A JSON representation of the playlist.
        """
        return self._post('playlists/', {'name': name,
                                         'privacy_level': 'instance'})

    def delete_playlist(self, id):
        """
        Delete a playlist from the server.

        :id: The Funkwhale id of the playlist.

        :return: An empty dictionary.
        """
        res = self._delete('playlists/%s/' % id)

        # manually remove cache entry, since it has a different path
        self.cache.remove('playlists/')

        return res

    def add_track_to_playlist(self, id, track):
        """
        Add a track to a playlist.

        :id: The Funkwhale id of the playlist.
        :tracks: The Funkwhale id of a track to add to the playlist.

        :return: A JSON response.
        """
        res = self._post('playlist-tracks/',
                         {'tracks': track, 'playlist': int(id)})

        # manually remove cache item, since it has a different path
        self.cache.remove('playlists/%s/tracks/' % id)

        return res

    def remove_track_from_playlist(self, id, track):
        """
        Remove a track from a playlist.

        :id: The Funkwhale id of the playlist.
        :track: The playlist id of the track to remove.

        :return: An empty dictionary.
        """
        res = self._delete('playlist-tracks/%s/' % track)

        # manually remove cache item, since it has a different path
        self.cache.remove('playlists/%s/tracks/' % id)

        return res

    def get_artists(self):
        """
        Get a paged list of artists on the server.

        :return: A JSON list of artists.
        """
        return self._get('artists/')

    def get_albums(self, id=None):
        """
        Get a paged list of albums, optionally from the given artist.

        :id: The Funkwhale id of the artist.

        :return: A list of all albums, or only albums from given artist.
        """
        path = 'albums/'
        # TODO better path manipulation
        if id:
            path += '?artist=%s' % id

        return self._get(path)

    def get_album(self, id):
        """
        Get a single album from the server.

        :id: The Funkwhale id of the album.

        :return: A JSON representation of the album.
        """
        return self._get('albums/%s/' % id)

    def get_album_tracks(self, id):
        """
        Get a single album's tracks from the server.

        :id: The Funkwhale id of the album.

        :return: A JSON list of tracks.
        """
        return self.get_album(id)['tracks']

    def load_all(self, json):
        """
        Load all content from a given paged result.

        :json: The paged list of items; must have a 'results' and 'next'.

        :return: A combined list of all paged content.
        """
        content = json['results']
        next_page = json['next']
        while next_page:
            json = self._get(next_page)
            content += json['results']
            next_page = json['next']
        return content
