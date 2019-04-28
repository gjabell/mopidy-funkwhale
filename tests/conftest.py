import pytest

from mopidy_funkwhale.backend import FunkwhaleBackend

FUNKWHALE_URL = "https://test.funkwhale"


@pytest.fixture
def config():
    return {
        "funkwhale": {
            "host": FUNKWHALE_URL,
            "user": "user",
            "password": "password",
            "cache_time": 3600,
        },
        "proxy": {}
    }


@pytest.fixture
def backend(config):
    return FunkwhaleBackend(config=config, audio=None)


@pytest.fixture
def playlists(backend):
    return backend.playlists


@pytest.fixture
def api(backend):
    backend.api.token = 'TOKEN'
    return backend.api


@pytest.fixture
def client(backend):
    return backend.client


@pytest.fixture
def mock_user():
    return {
        'id': 1,
        'username': 'user',
        'name': 'User',
        'date_joined': '2018-12-08T12:00:00Z',
        'avatar': {
            'square_crop': None,
            'small_square_crop': None,
            'original': None,
            'medium_square_crop': None
        }
    }


@pytest.fixture
def mock_track():
    return {
        'id': 1,
        'mbid': "f1e57531-e0df-4b3e-938f-1ae30c5b1a11",
        'title': "Do I Wanna Know?",
        'album': {
            'id': 1,
            'mbid': "bf584cf2-dc33-433e-b8b2-b85578822726",
            'title': "AM",
            'artist': {
                'id': 3,
                'mbid': "ada7a83c-e3e1-40f1-93f9-3e73dbc9298a",
                'name': "Arctic Monkeys",
                'creation_date': "2018-11-15T14:21:28.183506Z"
            },
            'release_date': "2013-09-10",
            'cover': {
                'square_crop': "",
                'small_square_crop': "",
                'original': "",
                'medium_square_crop': ""
            },
            'creation_date': "2018-11-15T14:21:28.186239Z"
        },
        'artist': {
            'id': 1,
            'mbid': "ada7a83c-e3e1-40f1-93f9-3e73dbc9298a",
            'name': "Arctic Monkeys",
            'creation_date': "2018-11-15T14:21:28.183506Z",
        },
        'creation_date': "2018-11-15T14:21:28.444129Z",
        'position': 1,
        'lyrics': "/api/v1/tracks/2/lyrics/",
        'is_playable': True,
        'uploads': [
            {
                'duration': 272,
                'bitrate': 320000,
                'listen_url':
                    "/api/v1/listen/17068209-06d6-4375-aa0f-916b2f58afa7/",
            }
        ],
        'size': 11006770,
        'mimetype': "audio/mpeg"
    }


@pytest.fixture
def mock_tracks(mock_track):
    return {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            mock_track
        ]
    }


@pytest.fixture
def mock_playlist_tracks(mock_track):
    return {
        'count': 1,
        'results': [
            {
                'id': 1,
                'track': mock_track,
                'playlist': 1,
                'index': 0,
                'creation_date': '2018-12-08T12:00:00Z'
            }
        ]
    }


@pytest.fixture
def mock_playlist(mock_user):
    return {
        'id': 1,
        'name': 'Test',
        'user': mock_user,
        'modification_date': '2018-12-08T12:00:00Z',
        'creation_date': '2018-12-08T12:00:00Z',
        'privacy_level': 'instance',
        'tracks_count': 1,
        'album_covers': [],
        'duration': 272
    }


@pytest.fixture
def mock_playlists(mock_playlist):
    return {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            mock_playlist
        ]
    }
