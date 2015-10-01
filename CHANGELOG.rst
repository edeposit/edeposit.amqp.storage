Changelog
=========

0.5.8
-----
    - Another attempt to solve problems with cached connections.

0.5.7
-----
    - Fixed bug in cached connection.

0.5.6
-----
    - Added custom 403 message.
    - Fixed bug in database connection caching.
    - Bottle's ``SimpleTemplate`` is now used instead of python's ``string.Template``.

0.5.5
-----
    - Added graceful exit to ``/bin/edeposit_storage_runzeo.sh`` which is required by supervisord.

0.5.0 - 0.5.4
-------------
    - ZIP Archives are now supported. They should result into creation of directory on disc.
    - Generator for generating structures rewritten to Bottle's templating engine.
    - Storage subsystem made universal.
    - Added Publication frontend over universal storage.
    - Added support for archives.
    - ``SearchResult.publications`` renamed to ``SearchResult.records``.
    - ``SaveRequest.pub`` renamed to ``SaveRequest.record``.
    - AMQP structure ``SaveRequest`` now returns proper ``Archive``/``Publication`` structure with just now saved metadata, without data.
    - Fixed bug in ``edeposit_storage_server.py``.
    - Fixed import bugs in ``edeposit_storage_server.py``.
    - #40: URL is now available even for private publications.
    - Quick unicode conversion fix.

0.4.0
-----
    - `BalancedDiscStorage <http://github.com/Bystroushaak/BalancedDiscStorage>`_ was put into place.
    - Serialization/deserialization of base64 content is now made using files, so it shouldn't take so much memory (copying of the string sometimes taked 3 times more than necessary).
    - File pointer is now transmitted back with metadata.

0.3.0
-----
    - Added support for UUID URL.
    - Added retreiving of the URL of the public documents.
    - Added example of the configuration files.

0.2.4
-----
    - Fixed MANIFEST.in to include default config files.

0.2.3
-----
    - `runzeo.sh` fixed and simplified.

0.2.2
-----
    - Added requirement to `zodbpickle`, which isn't installed automatically on suse for some strange reasons.
    - Fixed paths in `runzeo.sh` script.

0.2.1
-----
    - Small bugfix in settings.py.

0.2.0
-----
    - First working version.

0.1.0
-----
    - Project created.
