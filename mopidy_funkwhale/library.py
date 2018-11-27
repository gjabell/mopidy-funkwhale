from mopidy import backend

import logging
logger = logging.getLogger(__name__)

class FunkwhaleLibraryProvider(backend.LibraryProvider):
    root_directory = None

    def __init__(self, *args, **kwargs):
        super(FunkwhaleLibraryProvider, self).__init__(*args, **kwargs)

    def browse(uri):
        logger.warning('%s browse called' % __name__)

    def get_distinct(field, query=None):
        logger.warning('%s get_distinct called' % __name__)

    def get_images(uris):
        logger.warning('%s get_images called' % __name__)

    def lookup(uri):
        logger.warning('%s lookup called' % __name__)

    def refresh(uri):
        logger.warning('%s refresh called' % __name__)

    def search(query=None, uris=None, exact=False):
        logger.warning('%s search called' % __name__)

