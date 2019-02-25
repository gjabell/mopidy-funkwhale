import logging

from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhalePlaybackProvider(backend.PlaybackProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaybackProvider, self).__init__(*args, **kwargs)
        self.client = self.backend.client

    def translate_uri(self, uri):
        return self.client.get_playback(uri=uri)
