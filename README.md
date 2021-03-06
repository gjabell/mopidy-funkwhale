# Mopidy-Funkwhale

[![](https://img.shields.io/pypi/v/Mopidy-Funkwhale.svg?style=flat "Latest PyPI version")](https://pypi.python.org/pypi/Mopidy-Funkwhale/)
[![](https://travis-ci.com/gjabell/mopidy-funkwhale.svg?branch=master "Travis CI build status")](https://travis-ci.com/gjabell/mopidy-funkwhale)
[![Coverage Status](https://coveralls.io/repos/github/gjabell/mopidy-funkwhale/badge.svg?branch=master)](https://coveralls.io/github/gjabell/mopidy-funkwhale?branch=master)

Mopidy extension for connecting to a Funkwhale instance

**ABANDONED** This project has been abandoned, since I am no longer using Funkwhale. If you are interested in my current music setup, please take a look [at this post](https://galenabell.com/2019/08/15/an-open-music-setup/)!

Tested using Iris and ncmpcpp (mpd)

## Installation

There is no official `pip` package available at the moment, so this plugin can be installed directly from the repository via:

`pip install git+https://github.com/gjabell/mopidy-funkwhale.git`


## Configuration

Before starting Mopidy, you must add configuration for
Mopidy-Funkwhale to your Mopidy configuration file

```ini
[funkwhale]
host = https://test.funkwhale.com
user = test
password = badpassword
cache_time = 3600
```

The following configuration values are available:

- `funkwhale/enabled`: Whether the Funkwhale extension should be enabled. Defaults to `true`.
- `funkwhale/host`: The Funkwhale host to connect to. *Required*.
- `funkwhale/user`: The username used to connect to the host. *Required*.
- `funkwhale/password`: The password used to connect to the host. *Required*.
- `funkwhale/cache_time`: The number of seconds to cache data from the host. Defaults to `3600` (5 minutes).

## Project resources

- [Source code](https://github.com/gjabell/mopidy-funkwhale)
- [Issue tracker](https://github.com/gjabell/mopidy-funkwhale/issues)


## Credits

- Original author: [Galen Abell](https://github.com/gjabell)
- Current maintainer: [Galen Abell](https://github.com/gjabell)
- [Contributors](https://github.com/gjabell/mopidy-funkwhale/graphs/contributors)


## Roadmap

Playlists
  - [x] Load playlists
  - [x] Create new playlist
  - [x] Delete existing playlist
  - [x] Update existing playlist

Library
  - [x] Browse library
  - [ ] Search library

Playback
  - [x] Play songs

Favorites
  - [x] Play favorites
  - [x] Favorite songs
  - [x] Unfavorite songs


## Changelog

### v0.1.0 (UNRELEASED)

- Initial release.
