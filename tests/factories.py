# Modified from https://dev.funkwhale.audio/funkwhale/mopidy/
#                       blob/master/tests/factories.py

import factory

from mopidy import models


def timestr():
    return factory.Faker('date', pattern='%Y-%m-%dT%H:%M:%S.%fZ')


class ArtistJSONFactory(factory.Factory):
    id = factory.Sequence(int)
    mbid = factory.Faker("uuid4")
    name = factory.Faker("name")

    class Meta:
        model = dict


class ImageJSONFactory(factory.Factory):
    square_crop = factory.Faker('url')
    small_square_crop = factory.Faker('url')
    original = factory.Faker("url")
    medium_square_crop = factory.Faker("url")

    class Meta:
        model = dict


class AlbumJSONFactory(factory.Factory):
    id = factory.Sequence(int)
    mbid = factory.Faker("uuid4")
    title = factory.Faker("name")
    tracks = factory.Iterator([range(i) for i in range(1, 30)])
    artist = factory.SubFactory(ArtistJSONFactory)
    release_date = timestr()
    cover = factory.SubFactory(ImageJSONFactory)

    class Meta:
        model = dict


class TrackJSONFactory(factory.Factory):
    id = factory.Sequence(int)
    mbid = factory.Faker("uuid4")
    title = factory.Faker("name")
    position = factory.Faker("pyint")
    duration = factory.Faker("pyint")
    creation_date = timestr()
    bitrate = factory.Iterator([i * 1000 for i in (128, 256, 360)])
    artist = factory.SubFactory(ArtistJSONFactory)
    album = factory.SubFactory(AlbumJSONFactory)

    class Meta:
        model = dict


class UserJSONFactory(factory.Factory):
    id = factory.Sequence(int)
    username = factory.Faker('user_name')
    name = factory.Faker('name')
    date_joined = timestr()
    avatar = factory.SubFactory(ImageJSONFactory)

    class Meta:
        model = dict


class PlaylistJSONFactory(factory.Factory):
    id = factory.Sequence(int)
    name = factory.Faker('name')
    user = factory.SubFactory(UserJSONFactory)
    modification_date = timestr()
    creation_date = timestr()
    privacy_level = 'instance'
    tracks_count = 1
    album_covers = [factory.SubFactory(ImageJSONFactory)]
    duration = factory.Faker('pyint')

    class Meta:
        model = dict


class ArtistFactory(factory.Factory):
    class Meta:
        model = models.Artist
