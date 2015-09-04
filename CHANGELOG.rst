Changelog
=========

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
