Installation notes
==================

`Module <https://pypi.python.org/pypi/cz-urnnbn-api>`_ itself can be installed using PIP:

    sudo pip install edeposit.amqp.storage

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29

Configuration
-------------
After the installation, some configuration is required. Configuration is done using ``settings.py`` script, which reads data from configuration path ``~/edeposit/storage.json``.

Each uppercase attribute defined in :mod:`.settings` can be reconfigured using the ``storage.json`` configuration file.

Required configuration options is:

- :attr:`~storage.settings.PUBLIC_DIR`
- :attr:`~storage.settings.PRIVATE_DIR`

Highly recommended options:

- :attr:`~storage.settings.PRIVATE_INDEX`
- :attr:`~storage.settings.PRIVATE_INDEX_USERNAME`
- :attr:`~storage.settings.PRIVATE_INDEX_PASSWORD`
- :attr:`~storage.settings.WEB_ADDR`
- :attr:`~storage.settings.WEB_PORT`
- :attr:`~storage.settings.WEB_SERVER`

You should definitelly change the :attr:`~storage.settings.WEB_SERVER` to ``paste``. By default, the `wsgiref` backend is used, but that is only single-thread server. Paste will allow multithread access of users to your server.

Example of the configuration
----------------------------

::

    {
        "PUBLIC_DIR": "/var/edeposit_storage/public",
        "PRIVATE_DIR": "/var/edeposit_storage/private",
        "PRIVATE_INDEX": true,
        "PRIVATE_INDEX_PASSWORD": "secret password",
        "WEB_SERVER": "paste"
    }