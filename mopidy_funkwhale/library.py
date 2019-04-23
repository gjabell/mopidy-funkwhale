import logging

from mopidy import backend
from mopidy.models import Ref

import translator

logger = logging.getLogger(__name__)


class FunkwhaleLibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri='funkwhale:directory:root',
                                   name='Funkwhale')

    def __init__(self, *args, **kwargs):
        super(FunkwhaleLibraryProvider, self).__init__(*args, **kwargs)
        self.client = self.backend.client

    def browse(self, uri):
        # we have four levels:
        #   root dir ->
        #       artists ->
        #           albums ->
        #               tracks
        contents = []
        if translator.is_root_dir(uri):
            contents = [
                Ref.directory(uri='funkwhale:directory:artist:%s'
                                  % translator.get_id(a.uri),
                              name=a.name) for a in
                self.client.get_artists_refs()
            ]
        elif translator.is_artist_dir(uri):
            contents = [
                Ref.directory(uri='funkwhale:directory:album:%s'
                                  % translator.get_id(a.uri),
                              name=a.name) for a in
                self.client.get_albums_refs(uri=translator.get_id(uri))
            ]
        elif translator.is_album_dir(uri):
            contents = self.client.get_album_tracks_refs(
                uri=translator.get_id(uri))
        return contents

    def get_distinct(self, field, query=None):
        pass

    def get_images(self, uris):
        images = {}
        for uri in uris:
            image_list = []
            if translator.is_playlist_uri(uri):
                image_list += self.client.get_playlist_images(uri=uri)
            elif translator.is_album_uri(uri):
                image_list += self.client.get_album_images(uri=uri)
            images[uri] = image_list
        return images

    def lookup(self, uri=None, uris=None):
        if not uri and not uris:
            return []
        if uri is not None:
            uris = [uri]
        return self.client.get_tracks_list(uris=uris)

    def refresh(self, uri=None):
        pass

    def search(self, query=None, uris=None, exact=False):
        pass
