import mock

from mopidy_funkwhale import api, client, library, playback, playlists


def test_backend_has_scheme(backend):
    assert backend.uri_schemes == ['funkwhale']


def test_backend_has_providers(backend):
    assert isinstance(backend.api, api.FunkwhaleApi)
    assert isinstance(backend.client, client.FunkwhaleClient)
    assert isinstance(backend.library, library.FunkwhaleLibraryProvider)
    assert isinstance(backend.playback, playback.FunkwhalePlaybackProvider)
    assert isinstance(backend.playlists, playlists.FunkwhalePlaylistsProvider)


def test_backend_on_start_logs_in(backend):
    login_mock = mock.Mock()
    backend.api.login = login_mock

    backend.on_start()

    login_mock.assert_called_once()
