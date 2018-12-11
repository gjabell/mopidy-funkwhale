import mock

from mopidy_funkwhale import models
from mopidy_funkwhale.client import convert_uri

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
    client.api.get_playlists = lambda: [playlist]
    client.api.load_all = lambda _: [playlist]

    actual = client.get_playlists_refs()
    assert actual == [models.playlist_ref(playlist)]


def test_client_get_playlist_ref(client):
    playlist = factories.PlaylistJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_playlist = lambda _: playlist

    actual = client.get_playlist_ref(uri='')
    assert actual == models.playlist_ref(playlist)


def test_client_get_playlist(client):
    playlist = factories.PlaylistJSONFactory()
    tracks = [factories.TrackJSONFactory() for _ in
              range(playlist['tracks_count'])]
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


def test_client_get_playlist_items(client):
    track = factories.TrackJSONFactory()
    client.convert_uri = lambda: ''
    client.api.get_playlist_tracks = lambda _: [track]

    actual = client.get_playlist_items(uri='')
    assert actual == [models.track(track)]


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
