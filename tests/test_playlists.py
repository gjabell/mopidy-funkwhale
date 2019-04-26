import mock


def test_playlists_as_list_empty(playlists):
    refresh_mock = mock.Mock()
    playlists.refresh = refresh_mock

    assert playlists.as_list() == []
    refresh_mock.assert_called_once()


def test_playlists_as_list(playlists):
    def refresh(provider=playlists):
        provider.playlists = ['playlist']

    playlists.refresh = refresh

    assert playlists.as_list() == ['playlist']


def test_playlists_create(playlists):
    def refresh(provider=playlists):
        provider.playlists = ['playlist']

    playlists.refresh = refresh
    playlists.client.create_playlist = lambda p: p

    assert playlists.create('playlist') == 'playlist'


def test_playlists_delete_success(playlists):
    def refresh(provider=playlists):
        provider.playlists = []

    playlists.playlists = ['playlist']
    playlists.refresh = refresh
    playlists.client.delete_playlist = lambda uri=None: {}

    assert playlists.delete('uri')
    assert playlists.playlists == []


def test_playlists_delete_failure(playlists):
    playlists.playlists = ['playlist']
    playlists.refresh = mock.Mock()
    playlists.client.delete_playlist = lambda uri=None: None

    assert not playlists.delete('uri')
    assert playlists.playlists == ['playlist']


def test_playlists_get_items(playlists):
    playlists.client.get_playlist_items_refs = lambda uri=None: {}

    assert playlists.get_items('uri') == {}


def test_playlists_lookup(playlists):
    playlists.client.get_playlist = lambda uri=None: {}

    assert playlists.lookup('uri') == {}


def test_playlists_refresh(playlists):
    playlists.client.get_playlists_refs = lambda: ['playlist']

    assert playlists.playlists == []
    playlists.refresh()
    assert playlists.playlists == ['playlist']


def test_playlists_save(playlists):
    playlists.client.save_playlist = lambda _: 'playlist'

    assert playlists.save('playlist') == 'playlist'
