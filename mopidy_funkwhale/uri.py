import re

regex = re.compile(r'funkwhale://(\d+)')


def get_id(uri):
    return regex.match(uri).group(1)


def get_uri(i):
    return 'funkwhale://%d' % i
