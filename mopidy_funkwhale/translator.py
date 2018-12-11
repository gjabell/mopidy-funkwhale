import re

prefix = 'funkwhale'

album = 'album'
artist = 'artist'
playlist = 'playlist'
track = 'track'

regex = re.compile(r'(\w+):(\w+):(\d+)')


def get_id(uri):
    match = regex.match(uri)
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
