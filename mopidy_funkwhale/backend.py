import pykka

from mopidy_funkwhale import library, playback, playlists, api
from mopidy import backend


class FunkwhaleBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(FunkwhaleBackend, self).__init__()
        funkwhale_config = config['funkwhale']
        self.api = api.FunkwhaleApi(
            host=funkwhale_config['host'],
            user=funkwhale_config['user'],
            password=funkwhale_config['password'])
        self.audio = audio
        self.library = library.FunkwhaleLibraryProvider(backend=self)
        self.playback = playback.FunkwhalePlaybackProvider(audio=audio, backend=self)
        self.playlists = playlists.FunkwhalePlaylistsProvider(backend=self)
        self.uri_schemes = ['funkwhale']

