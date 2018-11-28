import logging
from mopidy import backend

logger = logging.getLogger(__name__)


class FunkwhaleLibraryProvider(backend.LibraryProvider):
    root_directory = None

    def __init__(self, *args, **kwargs):
        super(FunkwhaleLibraryProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api

    def browse(self, uri):
        logger.warning('%s browse called' % __name__)

    def get_distinct(self, field, query=None):
        logger.warning('%s get_distinct called' % __name__)

    def get_images(self, uris):
        logger.warning('%s get_images called' % __name__)

    def lookup(self, uri=None, uris=None):
        logger.warning('%s lookup called' % __name__)
        if not uri and not uris:
            return []
        if uri is not None:
            uris = [uri]
        return self.api.get_tracks(uris)

    def refresh(self, uri=None):
        logger.warning('%s refresh called' % __name__)

    def search(self, query=None, uris=None, exact=False):
        logger.warning('%s search called' % __name__)
