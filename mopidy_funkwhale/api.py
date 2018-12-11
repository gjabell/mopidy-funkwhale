import collections
import time

import logging
import requests
import urlparse
from mopidy import httpclient

import mopidy_funkwhale

logger = logging.getLogger(__name__)


# Modified from https://code.eliotberriot.com/funkwhale/mopidy/blob/master/mopidy_funkwhale/client.py
class SessionWithUrlBase(requests.Session):
    def __init__(self, url_base=None):
        super(SessionWithUrlBase, self).__init__()
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        if url.startswith("http://") or url.startswith("https://"):
            modified_url = url
        else:
            modified_url = urlparse.urljoin(self.url_base, url)
        return super(SessionWithUrlBase, self).request(method, modified_url, **kwargs)


def make_session(config):
    proxy = httpclient.format_proxy(config['proxy'])
    agent = httpclient.format_user_agent('%s/%s' % (
        mopidy_funkwhale.Extension.dist_name,
        mopidy_funkwhale.__version__))

    funkwhale_config = config['funkwhale']
    url = funkwhale_config['host']
    if not url.endswith('/'):
        url += '/'
    url += 'api/v1/'

    session = SessionWithUrlBase(url_base=url)
    session.proxies.update({'http': proxy, 'https': proxy})
    session.headers.update({'user-agent': agent})

    return session


# Modified from https://code.eliotberriot.com/funkwhale/mopidy/blob/master/mopidy_funkwhale/library.py
class Cache(collections.OrderedDict):
    def __init__(self, cache_time=3600):
        self.cache_time = cache_time
        super(Cache, self).__init__()

    def set(self, key, value):
        if not self.cache_time:
            return
        now = time.time()
        self[key] = (now, value)

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
        return v


class FunkwhaleApi:
    def __init__(self, config):
        self.session = make_session(config)
        self.token = None
        self.host = config['funkwhale']['host']
        self.username = config['funkwhale']['user']
        self.password = config['funkwhale']['password']
        self.cache = Cache(config['funkwhale']['cache_time'])

    def login(self):
        json = self._post('token/', {'username': self.username, 'password': self.password})
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

        json = r.json()
        self.cache.set(path, json)
        return json or {}

    def _post(self, path, body=None):
        body = body or {}

        r = self.session.post(path, data=body)
        r.raise_for_status()

        return r.json() or {}

    def get_playlists(self):
        return self._get('playlists/')

    def get_playlist(self, i):
        return self._get('playlists/%s/' % i)

    def get_playlist_tracks(self, i):
        # this endpoint returns a list of items in 'results', and each item contains a 'track' that doesn't have the
        # full track data, so we need to go get all the correct tracks based on that data
        partials = map(lambda x: x['track']['id'], self._get('playlists/%s/tracks/' % i)['results'])
        return [self.get_track(t) for t in partials]

    def get_tracks(self):
        return self._get('tracks/')

    def get_track(self, i):
        return self._get('tracks/%s/' % i)

    def get_playback(self, i):
        track = self.get_track(i)
        try:
            return '%s?jwt=%s' % (urlparse.urljoin(self.host, track['listen_url']), self.token)
        except KeyError:
            return None

    def load_all(self, json):
        content = json['results']
        next_page = json['next']
        while next_page:
            json = self._get(next_page)
            content += json['results']
            next_page = json['next']
        return content
