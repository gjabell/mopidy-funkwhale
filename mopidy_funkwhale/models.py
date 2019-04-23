import datetime

from mopidy.models import Album, Artist, Image, Playlist, Ref, Track

import translator


def album(json):
    return Album(
        uri=translator.get_album_uri(json['id']),
        name=json['title'],
        artists=[artist(json['artist'])],
        num_tracks=None,
        num_discs=None,
        date=json['release_date'],
        musicbrainz_id=json['mbid'],
        images=json['cover'].values())


def album_ref(json):
    return Ref.album(
        uri=translator.get_album_uri(json['id']),
        name=json['title'])


def album_json(album):
    return {
        'uri': album.uri,
        'name': album.name,
        'artists': [artist_json(a) for a in album.artists],
        'num_tracks': album.num_tracks,
        'num_discs': album.num_discs,
        'date': album.date,
        'musicbrainz_id': album.musicbrainz_id,
        'images': [i for i in album.images]
    }


def artist(json):
    return Artist(
        uri=translator.get_artist_uri(json['id']),
        name=json['name'],
        sortname=json['name'],
        musicbrainz_id=json['mbid'])


def artist_ref(json):
    return Ref.artist(
        uri=translator.get_artist_uri(json['id']),
        name=json['name'])


def artist_json(artist):
    return {
        'uri': artist.uri,
        'name': artist.name,
        'sortname': artist.sortname,
        'musicbrainz_id': artist.musicbrainz_id
    }


def playlist(json, tracks_json):
    tracks = []
    for t in tracks_json:
        cur = track(t['track'])
        if cur is not None:
            tracks += [cur]

    return Playlist(
        uri=translator.get_playlist_uri(json['id']),
        name=json['name'],
        tracks=tracks,
        last_modified=_jstime_to_unix(json['modification_date']))


def playlist_ref(json):
    return Ref.playlist(
        uri=translator.get_playlist_uri(json['id']),
        name=json['name'])


def playlist_json(playlist):
    return {
        'uri': playlist.uri,
        'name': playlist.name,
        'tracks': [track_json(t) for t in playlist.tracks],
        'last_modified': playlist.last_modified
    }


def track(json):
    uploads = json['uploads']
    if not uploads:
        return None

    return Track(
        uri=translator.get_track_uri(json['id']),
        name=json['title'],
        artists=[artist(json['artist'])],
        album=album(json['album']),
        composers=[],
        performers=[],
        genre='',
        track_no=json['position'],
        disc_no=None,
        date='',
        length=uploads[0]['duration'] * 1000,
        bitrate=uploads[0]['bitrate'],
        comment='',
        musicbrainz_id=json['mbid'],
        last_modified=_jstime_to_unix(json['creation_date']))


def track_ref(json):
    return Ref.track(
        uri=translator.get_track_uri(json['id']),
        name=json['title'])


def track_json(track):
    return {
        'uri': track.uri,
        'name': track.name,
        'artists': [artist_json(a) for a in track.artists],
        'album': album_json(track.album),
        'composers': [],
        'performers': [],
        'genre': track.genre,
        'track_no': track.track_no,
        'disc_no': track.disc_no,
        'date': track.date,
        'length': track.length,
        'bitrate': track.bitrate,
        'comment': track.comment,
        'musicbrainz_id': track.musicbrainz_id,
        'last_modified': track.last_modified
    }


def image(json):
    return Image(
        uri=json,
        height=None,
        width=None)


def _jstime_to_unix(t):
    date = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    return int(date.strftime('%s'))
