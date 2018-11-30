import logging
from mopidy import backend
from mopidy.models import Ref

logger = logging.getLogger(__name__)


class FunkwhaleLibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='funkwhale:directory', name='Funkwhale')

    def __init__(self, *args, **kwargs):
        super(FunkwhaleLibraryProvider, self).__init__(*args, **kwargs)
        self.api = self.backend.api
        self.verbose = self.backend.verbose

    def browse(self, uri):
        if self.verbose:
            logger.warning('%s browse called' % __name__)

    def get_distinct(self, field, query=None):
        if self.verbose:
            logger.warning('%s get_distinct called' % __name__)

    def get_images(self, uris):
        if self.verbose:
            logger.warning('%s get_images called' % __name__)

    def lookup(self, uri=None, uris=None):
        if self.verbose:
            logger.warning('%s lookup called' % __name__)
        if not uri and not uris:
            return []
        if uri is not None:
            uris = [uri]
        return self.api.get_tracks_list(uris)

    def refresh(self, uri=None):
        if self.verbose:
            logger.warning('%s refresh called' % __name__)

    def search(self, query=None, uris=None, exact=False):
        if self.verbose:
            logger.warning('%s search called' % __name__)
