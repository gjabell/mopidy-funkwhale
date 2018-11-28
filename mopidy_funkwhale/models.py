import datetime

from mopidy.models import Album, Artist, Playlist, Ref, Track

import uri


def album(data):
    return Album(
        uri=uri.get_uri(data['id']),
        name=data['title'],
        artists=[artist(data['artist'])],
        num_tracks=None,
        num_discs=None,
        date=data['release_date'],
        musicbrainz_id=data['mbid'],
        images=data['cover'])


def album_ref(data):
    return Ref.album(
        uri=uri.get_uri(data['id']),
        name=data['name'])


def artist(data):
    return Artist(
        uri=uri.get_uri(data['id']),
        name=data['name'],
        sortname=data['name'],
        musicbrainz_id=data['mbid'])


def artist_ref(data):
    return Ref.artist(
        uri=uri.get_uri(data['id']),
        name=data['name'])


def playlist(data, tracks_data):
    return Playlist(
        uri=uri.get_uri(data['id']),
        name=data['name'],
        tracks=[track(t) for t in tracks_data],
        last_modified=_jstime_to_unix(data['modification_date']))


def playlist_ref(data):
    return Ref.playlist(
        uri=uri.get_uri(data['id']),
        name=data['name'])


def track(data):
    return Track(
        uri=uri.get_uri(data['id']),
        name=data['title'],
        artists=[artist(data['artist'])],
        album=album(data['album']),
        composers=[],
        performers=[],
        genre='',
        track_no=data['position'],
        disc_no=None,
        date='',
        length=None,
        bitrate=0,
        comment='',
        musicbrainz_id=data['mbid'],
        last_modified=_jstime_to_unix(data['creation_date']))


def track_ref(data):
    return Ref.track(
        uri=uri.get_uri(data['id']),
        name=data['title'])


def _jstime_to_unix(t):
    date = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    return int(date.strftime('%s'))
