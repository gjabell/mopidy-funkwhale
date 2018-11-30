import logging
from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhalePlaybackProvider(backend.PlaybackProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaybackProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api
        self.verbose = self.backend.verbose

    def translate_uri(self, uri):
        if self.verbose:
            logger.warning('%s translate_uri called' % __name__)
        translated = self.api.get_playback(uri)
        if self.verbose:
            logger.warning('translated %s -> %s' % (uri, translated))
        return translated
