import datetime

from mopidy.models import Album, Artist, Playlist, Ref, Track

import translator


def album(data):
    return Album(
        uri=translator.get_album_uri(data['id']),
        name=data['title'],
        artists=[artist(data['artist'])],
        num_tracks=None,
        num_discs=None,
        date=data['release_date'],
        musicbrainz_id=data['mbid'],
        images=data['cover'])


def album_ref(data):
    return Ref.album(
        uri=translator.get_album_uri(data['id']),
        name=data['name'])


def artist(data):
    return Artist(
        uri=translator.get_artist_uri(data['id']),
        name=data['name'],
        sortname=data['name'],
        musicbrainz_id=data['mbid'])


def artist_ref(data):
    return Ref.artist(
        uri=translator.get_artist_uri(data['id']),
        name=data['name'])


def playlist(data, tracks_data):
    return Playlist(
        uri=translator.get_playlist_uri(data['id']),
        name=data['name'],
        tracks=[track(t) for t in tracks_data],
        last_modified=_jstime_to_unix(data['modification_date']))


def playlist_ref(data):
    return Ref.playlist(
        uri=translator.get_playlist_uri(data['id']),
        name=data['name'])


def track(data):
    return Track(
        uri=translator.get_track_uri(data['id']),
        name=data['title'],
        artists=[artist(data['artist'])],
        album=album(data['album']),
        composers=[],
        performers=[],
        genre='',
        track_no=data['position'],
        disc_no=None,
        date='',
        length=data['duration'] * 1000,
        bitrate=data['bitrate'],
        comment='',
        musicbrainz_id=data['mbid'],
        last_modified=_jstime_to_unix(data['creation_date']))


def track_ref(data):
    return Ref.track(
        uri=translator.get_track_uri(data['id']),
        name=data['title'])


def _jstime_to_unix(t):
    date = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    return int(date.strftime('%s'))
