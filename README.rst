****************************
Mopidy-Funkwhale
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Funkwhale.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Funkwhale/
    :alt: Latest PyPI version

.. image:: https://travis-ci.com/gjabell/mopidy-funkwhale.svg?branch=master
    :target: https://travis-ci.com/gjabell/mopidy-funkwhale
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/gjabell/mopidy-funkwhale/badge.svg
    :target: https://coveralls.io/github/gjabell/mopidy-funkwhale
    :alt: Test coverage


Mopidy extension for connecting to a Funkwhale instance


Installation
============

There is no official ``pip`` package available at the moment, so this plugin can be installed directly from the repository via:

``pip install git+https://github.com/gjabell/mopidy-funkwhale.git``


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Funkwhale to your Mopidy configuration file::

    [funkwhale]
    host = https://test.funkwhale.com
    user = test
    password = badpassword
    cache_time = 3600
    verbose = false

The following configuration values are available:

- ``funkwhale/enabled``: Whether the Funkwhale extension should be enabled. Defaults to ``true``.
- ``funkwhale/host``: The Funkwhale host to connect to. *Required*.
- ``funkwhale/user``: The username used to connect to the host. *Required*.
- ``funkwhale/password``: The password used to connect to the host. *Required*.
- ``funkwhale/cache_time``: The number of seconds to cache data from the host. Defaults to ``3600`` (5 minutes).
- ``funkwhale/verbose``: Whether to print verbose logs (may help with debugging). Defaults to ``false``.

Project resources
=================

- `Source code <https://github.com/gjabell/mopidy-funkwhale>`_
- `Issue tracker <https://github.com/gjabell/mopidy-funkwhale/issues>`_


Credits
=======

- Original author: `Galen Abell <https://github.com/gjabell>`__
- Current maintainer: `Galen Abell <https://github.com/gjabell>`__
- `Contributors <https://github.com/gjabell/mopidy-funkwhale/graphs/contributors>`_


Roadmap
========

- Playlists
  [x] Load playlists
  [x] Create new playlist
  [x] Delete existing playlist
  [x] Update existing playlist

- Library
  [ ] Browse library
  [ ] Search library

- Playback
  [x] Play songs


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
