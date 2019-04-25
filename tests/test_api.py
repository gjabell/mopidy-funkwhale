def test_api_get_playlists(api, requests_mock, mock_playlists):
    requests_mock.get(api.session.url_base + "playlists/", json=mock_playlists)

    actual = api.get_playlists()
    assert actual == mock_playlists


def test_api_get_playlist(api, requests_mock, mock_playlist):
    requests_mock.get(api.session.url_base + "playlists/1/",
                      json=mock_playlist)

    actual = api.get_playlist(1)
    assert actual == mock_playlist


def test_api_get_playlist_tracks(api, requests_mock, mock_playlist_tracks):
    requests_mock.get(api.session.url_base + 'playlists/1/tracks/',
                      json=mock_playlist_tracks)

    actual = api.get_playlist_tracks(1)
    assert actual == mock_playlist_tracks['results']


def test_api_get_tracks(api, requests_mock, mock_tracks):
    requests_mock.get(api.session.url_base + "tracks/", json=mock_tracks)

    actual = api.get_tracks()
    assert actual == mock_tracks


def test_api_get_track(api, requests_mock, mock_track):
    requests_mock.get(api.session.url_base + "tracks/1/", json=mock_track)

    actual = api.get_track(1)
    assert actual == mock_track


def test_api_get_favorite_tracks(api, requests_mock, mock_tracks):
    requests_mock.get(api.session.url_base + 'favorites/tracks/',
                      json=mock_tracks)

    actual = api.get_favorite_tracks()
    assert actual == mock_tracks
    assert api.cache.get('favorites/tracks/') == mock_tracks


def test_api_favorite_track(api, requests_mock):
    expected = {'id': 1, 'track': 1}
    api.cache.set('favorites/tracks/', expected)
    requests_mock.post(api.session.url_base + 'favorites/tracks/',
                       json=expected)

    actual = api.favorite_track(1)
    assert actual == expected
    assert api.cache.get('favorites/tracks/') is None


def test_api_unfavorite_track(api, requests_mock):
    api.cache.set('favorites/tracks/', {})
    requests_mock.post(api.session.url_base + 'favorites/tracks/remove/',
                       json={})

    actual = api.unfavorite_track(1)
    assert actual == {}
    assert api.cache.get('favorites/tracks/') is None


def test_api_get_playback(api, requests_mock, mock_track):
    requests_mock.get(api.session.url_base + "tracks/1/", json=mock_track)

    actual = api.get_playback(1)
    assert actual == 'https://test.funkwhale/api/v1/listen/' \
                     '17068209-06d6-4375-aa0f-916b2f58afa7/?jwt=TOKEN'


def test_api_create_playlist(api, requests_mock, mock_playlist):
    requests_mock.post(api.session.url_base + 'playlists/', json=mock_playlist)

    actual = api.create_playlist('Test')
    assert actual == mock_playlist


def test_api_delete_playlist(api, requests_mock, mock_playlist):
    api.cache.set('playlists/1/', {})
    requests_mock.delete(api.session.url_base + 'playlists/1/')

    actual = api.delete_playlist('1')
    assert actual == {}
    assert api.cache.get('playlists/1/') is None


def test_api_add_track_to_playlist(api, requests_mock):
    expected = {'id': 1, 'track': 1, 'playlist': 1, 'index': 1}
    api.cache.set('playlists/1/tracks/', [])
    requests_mock.post(api.session.url_base + 'playlist-tracks/',
                       json=expected)

    actual = api.add_track_to_playlist(1, 1)
    assert actual == expected
    assert api.cache.get('playlists/1/tracks/') is None


def test_api_remove_track_from_playlist(api, requests_mock):
    api.cache.set('playlists/1/tracks/', [])
    requests_mock.delete(api.session.url_base + 'playlist-tracks/1/', json={})

    actual = api.remove_track_from_playlist(1, 1)
    assert actual == {}
    assert api.cache.get('playlists/1/tracks/') is None


def test_api_load_all_single(api):
    first = {'count': 1, 'results': [1], 'next': None, 'previous': None}

    actual = api.load_all(first)
    assert actual == [1]


def test_api_load_all_multiple(api, requests_mock):
    first = {'count': 3, 'results': [1], 'next': 'https://second',
             'previous': None}
    second = {'count': 3, 'results': [2], 'next': 'https://third',
              'previous': 'https://first'}
    third = {'count': 3, 'results': [3], 'next': None,
             'previous': 'https://second'}

    requests_mock.get('https://second', json=second)
    requests_mock.get('https://third', json=third)

    actual = api.load_all(first)
    assert actual == [1, 2, 3]
