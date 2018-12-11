from __future__ import unicode_literals

from mopidy_funkwhale import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert '[funkwhale]' in config
    assert 'enabled = true' in config
    assert 'host =' in config
    assert 'user =' in config
    assert 'password =' in config
    assert 'cache_time = 3600' in config
    assert 'verbose = false' in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    assert 'host' in schema
    assert 'user' in schema
    assert 'password' in schema
    assert 'cache_time' in schema
    assert 'verbose' in schema
