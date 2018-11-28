from mopidy.models import Album, Artist, Playlist, Ref, Track


def album(json):
    return Album(
            uri=str(json['id']),
            name=json['name'],
            artists=[artist(json['artist'])],
            num_tracks=None,
            num_discs=None
            date=json['release_date'],
            musicbrainz_id=json['mbid'],
            images=json['cover'])


def album_ref(json):
    return Ref.album(
            uri=str(json['id']),
            name=json['name'])


def artist(json):
    return Artist(
            uri=str(json['id']),
            name=json['name'],
            sortname=json['name'],
            musicbrainz_id=json['mbid'])


def artist_ref(json):
    return Ref.artist(
            uri=str(json['id']),
            name=json['name'])


def playlist(json, tracks_json):
    return Playlist(
            uri=str(json['id']),
            name=json['name'],
            tracks=[track(track) for track in tracks_json],
            last_modified=_jstime_to_unix(json['modification_date']))


def playlist_ref(json):
    return Ref.playlist(
            uri=str(json['id']),
            name=json['name'])


def track(json):
    return Track(
            uri=str(json['id']),
            name=json['title'],
            artists=[artist(json['artist'])],
            album=album(json['album']),
            composers=[],
            performers=[],
            genre='',
            track_no=json['position'],
            disc_no=None,
            date='',
            length=None,
            bitrate=0,
            comment='',
            musicbrainz_id=json['mbid'],
            last_modified=_jstime_to_unix(json['creation_date']))


def track_ref(json):
    return Ref.track(
            uri=str(json['id']),
            name=json['title'])


def _jstime_to_unix(t):
    return int(datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ').strftime('%s'))

