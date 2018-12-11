****************************
Mopidy-Funkwhale
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Funkwhale.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Funkwhale/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/gjabell/mopidy-funkwhale/master.svg?style=flat
    :target: https://travis-ci.com/gjabell/mopidy-funkwhale
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/gjabell/mopidy-funkwhale/badge.svg
    :target: https://coveralls.io/github/gjabell/mopidy-funkwhale
    :alt: Test coverage


Mopidy extension for connecting to a Funkwhale instance


Installation
============

Install by running::

    pip install Mopidy-Funkwhale

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Funkwhale to your Mopidy configuration file::

    [funkwhale]
    host = https://test.funkwhale.com
    user = test
    password = badpassword
    cache_time = 3600
    verbose = false

The following configuration values are available:

- `funkwhale/enabled`: Whether the Funkwhale extension should be enabled. Defaults to `true`.
- `host`: The Funkwhale host to connect to. *Required*.
- `user`: The username used to connect to the host. *Required*.
- `password`: The password used to connect to the host. *Required*.
- `cache_time`: The number of seconds to cache data from the host. Defaults to `3600` (5 minutes).
- `verbose`: Whether to print verbose logs (may help with debugging). Defaults to `false`.

Project resources
=================

- `Source code <https://github.com/gjabell/mopidy-funkwhale>`_
- `Issue tracker <https://github.com/gjabell/mopidy-funkwhale/issues>`_


Credits
=======

- Original author: `Galen Abell <https://github.com/gjabell>`__
- Current maintainer: `Galen Abell <https://github.com/gjabell>`__
- `Contributors <https://github.com/gjabell/mopidy-funkwhale/graphs/contributors>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
