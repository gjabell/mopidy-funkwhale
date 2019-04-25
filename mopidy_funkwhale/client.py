from datetime import datetime as dt
import logging

import models

import mopidy_funkwhale

import translator

logger = logging.getLogger(__name__)


favorites_id = -1


favorites_ref = {
    'id': -1,
    'name': 'Favorites'
}
favorites_playlist = {
    'id': -1,
    'name': 'Favorites',
    'modification_date': dt.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
}


def _is_favorites(id):
    return id and int(id) == favorites_id


def convert_uri(fn):
    def _wrapper(*args, **kwargs):
        for k, v in kwargs.iteritems():
            if k == 'uri':
                kwargs[k] = translator.get_id(v)
            elif k == 'uris':
                kwargs[k] = [translator.get_id(u) for u in v]
        return fn(*args, **kwargs)

    return _wrapper


class FunkwhaleClient(object):
    def __init__(self, api):
        self.api = api

    def get_playlists_refs(self):
        return [models.playlist_ref(p) for p in
                self.api.load_all(self.api.get_playlists()) +
                [favorites_ref]]  # also insert the favorites 'playlist'

    @convert_uri
    def get_playlist_ref(self, uri=None):
        ref = (favorites_ref
               if _is_favorites(uri)
               else self.api.get_playlist(uri))

        return models.playlist_ref(ref)

    @convert_uri
    def get_playlist(self, uri=None):
        playlist = (favorites_playlist
                    if _is_favorites(uri)
                    else self.api.get_playlist(uri))
        tracks = (self.api.load_all(self.api.get_favorite_tracks())
                  if _is_favorites(uri)
                  else self.api.get_playlist_tracks(uri))

        return models.playlist(playlist, tracks)

    @convert_uri
    def get_playlist_items_refs(self, uri=None):
        tracks = (self.api.load_all(self.api.get_favorite_tracks())
                  if _is_favorites(uri)
                  else self.api.get_playlist_tracks(uri))

        return [models.track_ref(t) for t in tracks]

    @convert_uri
    def get_playlist_images(self, uri=None):
        images = ([]
                  if _is_favorites(uri)
                  else self.api.get_playlist(uri)['album_covers'])

        return [models.Image(i) for i in images]

    @convert_uri
    def get_track(self, uri=None):
        return models.track(self.api.get_track(uri))

    @convert_uri
    def get_tracks_list(self, uris=None):
        # TODO might be a better endpoint for multiple tracks
        return [models.track(t) for t in [self.api.get_track(u) for u in uris]]

    @convert_uri
    def get_playback(self, uri=None):
        return self.api.get_playback(uri)

    def create_playlist(self, name):
        return models.playlist(self.api.create_playlist(name), [])

    @convert_uri
    def delete_playlist(self, uri=None):
        return self.api.delete_playlist(uri)

    def save_playlist(self, playlist):
        playlist_id = mopidy_funkwhale.translator.get_id(playlist.uri)
        # get an up-to-date copy of the server playlist
        server_playlist = (self.api.load_all(self.api.get_favorite_tracks())
                           if _is_favorites(playlist_id) else
                           self.api.get_playlist_tracks(playlist_id))

        # get a list of all track ids in the server playlist
        server_ids = [str(t['track']['id']) for t in server_playlist]
        # each track has an id for the entire application, but each playlist
        # stores a unique id per track as well
        # the delete method requires us to pass the playlist's id of the track,
        # so here we create a map between the two
        server_playlist_id_map = {str(t['track']['id']): str(t['id'])
                                  for t in server_playlist}

        # get a list of all track ids in the client playlist
        client_ids = [mopidy_funkwhale.translator.get_id(t.uri)
                      for t in playlist.tracks]

        # diff the lists to know which tracks to add and which to delete
        tracks_to_add = [t for t in client_ids if t not in server_ids]
        tracks_to_del = [t for t in server_ids if t not in client_ids]

        for track in tracks_to_add:
            if _is_favorites(playlist_id):
                self.api.favorite_track(track)
            else:
                self.api.add_track_to_playlist(playlist_id, track)
        for track in tracks_to_del:
            if _is_favorites(playlist_id):
                self.api.unfavorite_track(track)
            else:
                self.api.remove_track_from_playlist(playlist_id,
                                                    server_playlist_id_map[
                                                        track])

        # load the new server version of the playlist
        return self.get_playlist(uri=playlist.uri)

    def get_artists_refs(self):
        return [models.artist_ref(a) for a in
                self.api.load_all(self.api.get_artists())]

    def get_albums_refs(self, uri=None):
        return [models.album_ref(a) for a in
                self.api.load_all(self.api.get_albums(id=uri))]

    @convert_uri
    def get_album_images(self, uri=None):
        return [models.image(i) for i in
                self.api.get_album(id=uri)['cover']['original']]

    def get_album_tracks_refs(self, uri=None):
        return [models.track_ref(t) for t in
                self.api.get_album_tracks(uri)]
