"""
This module provides URI translation between Mopidy and Funkwhale.
"""

import re

prefix = 'funkwhale'

album = 'album'
artist = 'artist'
playlist = 'playlist'
track = 'track'
directory = 'directory'

uri_regex = re.compile(r'(\w+):(\w+:?\w+?):(\d+)')
uri_format = r'%s:%%s:%%d' % prefix
dir_format = r'%s:%s:%%s:(\d+)' % (prefix, directory)


def get_id(uri):
    match = uri_regex.match(uri)
    if not match:
        return None
    return match.group(3)


def get_uri(t, i):
    return '%s:%s:%d' % (prefix, t, i)


def get_album_uri(i):
    return get_uri(album, i)


def get_artist_uri(i):
    return get_uri(artist, i)


def get_playlist_uri(i):
    return get_uri(playlist, i)


def get_track_uri(i):
    return get_uri(track, i)


def is_artist_uri(uri):
    return re.match(uri_format % artist, uri) is not None


def is_album_uri(uri):
    return re.match(uri_format % album, uri) is not None


def is_track_uri(uri):
    return re.match(uri_format % track, uri) is not None


def is_playlist_uri(uri):
    return re.match(uri_format % playlist, uri) is not None


def is_root_dir(uri):
    return uri == 'funkwhale:directory:root'


def is_artist_dir(uri):
    return re.match(dir_format % artist, uri) is not None


def is_album_dir(uri):
    return re.match(dir_format % album, uri) is not None


def is_track_dir(uri):
    return re.match(dir_format % track, uri) is not None
