import logging
from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhalePlaybackProvider(backend.PlaybackProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaybackProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api

    def translate_uri(self, uri):
        logger.warning('%s translate_uri called' % __name__)
        return self.api.get_playback(uri)
