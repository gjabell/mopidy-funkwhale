import mock

import mopidy_funkwhale
from mopidy_funkwhale import models
from mopidy_funkwhale.client import (convert_uri,
                                     favorites_playlist)

from tests import factories


@mock.patch('mopidy_funkwhale.client.translator')
def test_client_convert_uri_uri(translator):
    @convert_uri
    def fn(uri=None):
        return uri

    fn(uri='test')

    translator.get_id.assert_called_once_with('test')


@mock.patch('mopidy_funkwhale.client.translator')
def test_client_convert_uri_uris(translator):
    @convert_uri
    def fn(uris=None):
        return uris

    fn(uris=['test', 'test2'])

    translator.get_id.assert_has_calls([mock.call('test'), mock.call('test2')])


def test_client_get_playlists_refs(client):
    playlist = factories.PlaylistJSONFactory()
    client.api.get_playlists = lambda: [playlist, favorites_playlist]
    client.api.load_all = lambda _: [playlist]

    actual = client.get_playlists_refs()
    assert actual == [models.playlist_ref(playlist),
                      models.playlist_ref(favorites_playlist)]


def test_client_get_playlist_ref(client):
    playlist = factories.PlaylistJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_playlist = lambda _: playlist

    actual = client.get_playlist_ref(uri='')
    assert actual == models.playlist_ref(playlist)


def test_client_get_playlist(client):
    playlist = factories.PlaylistJSONFactory()
    tracks = [{
            'id': t['id'],
            'track': t
        } for t in [factories.TrackJSONFactory() for _ in
                    range(playlist['tracks_count'])]
    ]
    client.convert_uri = lambda: ''
    client.api.get_playlist = lambda _: playlist
    client.api.get_playlist_tracks = lambda _: tracks

    actual = client.get_playlist(uri='')
    assert actual == models.playlist(playlist, tracks)


def test_client_get_playlist_items_ref(client):
    track = factories.TrackJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_playlist_tracks = lambda _: [track]

    actual = client.get_playlist_items_refs(uri='')
    assert actual == [models.track_ref(track)]


def test_client_get_track(client):
    track = factories.TrackJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_track = lambda _: track

    actual = client.get_track(uri='')
    assert actual == models.track(track)


def test_client_get_tracks_list(client):
    track = factories.TrackJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_track = lambda _: track

    actual = client.get_tracks_list(uris=[''])
    assert actual == [models.track(track)]


def test_client_get_playback(client):
    client.convert_uri = lambda: ''
    client.api.get_playback = lambda _: 'uri'

    actual = client.get_playback(uri='uri')
    assert actual == 'uri'


def test_client_save_playlist_add_track(client, requests_mock):
    playlist = factories.PlaylistFactory()
    playlist_id = int(playlist.uri)
    json_tracklist = [{
            'id': t['id'],
            'track': t
        } for t in [factories.TrackJSONFactory() for _ in
                    range(0, 10)]
    ]

    new_track = mopidy_funkwhale.models.track(factories.TrackJSONFactory())
    # mopidy models are immutable, so we need to make a new playlist
    tracklist = tuple(mopidy_funkwhale.models.track(json['track'])
                      for json in json_tracklist)
    local_playlist = models.Playlist(
            uri=mopidy_funkwhale.translator.get_playlist_uri(playlist_id),
            name=playlist.name,
            tracks=tracklist + (new_track, ),
            last_modified=playlist.last_modified)

    add_mock = mock.Mock()
    del_mock = mock.Mock()
    favorite_mock = mock.Mock()
    unfavorite_mock = mock.Mock()

    client.api.add_track_to_playlist = add_mock
    client.api.remove_track_from_playlist = del_mock
    client.api.favorite_track = favorite_mock
    client.api.unfavorite_track = unfavorite_mock
    client.get_playlist = lambda uri=None: local_playlist
    client.api.get_playlist_tracks = lambda _: json_tracklist

    actual = client.save_playlist(local_playlist)

    assert actual == local_playlist
    add_mock.assert_called_with(str(playlist_id),
                                mopidy_funkwhale.translator.get_id(
                                    new_track.uri))
    del_mock.assert_not_called()
    favorite_mock.assert_not_called()
    unfavorite_mock.assert_not_called()


def test_client_save_playlist_remove_track(client, requests_mock):
    playlist = factories.PlaylistFactory()
    playlist_id = int(playlist.uri)
    json_tracklist = [{
            'id': t['id'],
            'track': t
        } for t in [factories.TrackJSONFactory() for _ in
                    range(0, 10)]
    ]

    track_to_del = json_tracklist.pop(-1)
    tracklist = tuple(mopidy_funkwhale.models.track(json['track'])
                      for json in json_tracklist)
    local_playlist = models.Playlist(
            uri=mopidy_funkwhale.translator.get_playlist_uri(playlist_id),
            name=playlist.name,
            tracks=tracklist,
            last_modified=playlist.last_modified)

    add_mock = mock.Mock()
    del_mock = mock.Mock()
    favorite_mock = mock.Mock()
    unfavorite_mock = mock.Mock()

    client.api.add_track_to_playlist = add_mock
    client.api.remove_track_from_playlist = del_mock
    client.api.favorite_track = favorite_mock
    client.api.unfavorite_track = unfavorite_mock
    client.get_playlist = lambda uri=None: local_playlist
    client.api.get_playlist_tracks = lambda _: json_tracklist + [track_to_del]

    actual = client.save_playlist(local_playlist)

    assert actual == local_playlist
    add_mock.assert_not_called()
    del_mock.assert_called_with(str(playlist_id), str(track_to_del['id']))
    favorite_mock.assert_not_called()
    unfavorite_mock.assert_not_called()
