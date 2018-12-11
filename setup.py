from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Funkwhale',
    version=get_version('mopidy_funkwhale/__init__.py'),
    url='https://github.com/gjabell/mopidy-funkwhale',
    license='Apache License, Version 2.0',
    author='Galen Abell',
    author_email='galen@galenabell.com',
    description='Mopidy extension for connecting to a Funkwhale instance',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
        'requests >= 2.0'
    ],
    entry_points={
        'mopidy.ext': [
            'funkwhale = mopidy_funkwhale:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
