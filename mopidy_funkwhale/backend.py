import pykka
from mopidy import backend

from mopidy_funkwhale import library, playback, playlists, api, client


class FunkwhaleBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(FunkwhaleBackend, self).__init__()
        self.verbose = False
        self.api = api.FunkwhaleApi(config)
        self.client = client.FunkwhaleClient(self.api)
        self.audio = audio
        self.library = library.FunkwhaleLibraryProvider(backend=self)
        self.playback = playback.FunkwhalePlaybackProvider(audio=audio, backend=self)
        self.playlists = playlists.FunkwhalePlaylistsProvider(backend=self)
        self.uri_schemes = ['funkwhale']

    def on_start(self):
        self.api.login()
