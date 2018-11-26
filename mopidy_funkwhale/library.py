from mopidy import backend

import logging
logger = logging.getLogger(__name__)

class FunkwhaleLibraryProvider(backend.LibraryProvider):
    def __init__(self, *args, **kwargs):
        super(FunkwhaleLibraryProvider, self).__init__(*args, **kwargs)

