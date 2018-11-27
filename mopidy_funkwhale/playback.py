from mopidy import backend

import logging
logger = logging.getLogger(__name__)

class FunkwhalePlaybackProvider(backend.PlaybackProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhalePlaybackProvider, self).__init__(*args, **kwargs)

    def translate_uri(self, uri):
        logger.warning('%s translate_uri called' % __name__)
        return None
