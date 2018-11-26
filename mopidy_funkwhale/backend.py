import pykka

from mopidy_funkwhale import playlists, api
from mopidy import backend


class FunkwhaleBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(FunkwhaleBackend, self).__init__()
        self.api = api.FunkwhaleApi()
        self.audio = audio
        self.playlists = playlists.FunkwhalePlaylistsProvider(backend=self)

