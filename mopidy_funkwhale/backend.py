import pykka
import requests
from mopidy import backend, httpclient

import mopidy_funkwhale
from mopidy_funkwhale import library, playback, playlists, api


class FunkwhaleBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(FunkwhaleBackend, self).__init__()
        self.verbose = False
        self.session = make_session(config)
        funkwhale_config = config['funkwhale']
        self.api = api.FunkwhaleApi(
            host=funkwhale_config['host'],
            session=self.session)
        self.audio = audio
        self.library = library.FunkwhaleLibraryProvider(backend=self)
        self.playback = playback.FunkwhalePlaybackProvider(audio=audio, backend=self)
        self.playlists = playlists.FunkwhalePlaylistsProvider(backend=self)
        self.uri_schemes = ['funkwhale']


def make_session(config):
    proxy = httpclient.format_proxy(config['proxy'])
    agent = httpclient.format_user_agent('%s/%s' % (
        mopidy_funkwhale.Extension.dist_name,
        mopidy_funkwhale.__version__))
    funkwhale_config = config['funkwhale']
    auth = (funkwhale_config['user'], funkwhale_config['password'])

    session = requests.Session()
    session.proxies.update({'http': proxy, 'https': proxy})
    session.headers.update({'user-agent': agent})
    session.auth = auth  # TODO use jwt

    return session
