Installation notes
==================

`Module <https://pypi.python.org/pypi/cz-urnnbn-api>`_ itself can be installed using PIP::

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
- :attr:`~storage.settings.ZCONF_PATH`

You should definitelly change the :attr:`~storage.settings.WEB_SERVER` to ``paste``. By default, the `wsgiref` backend is used, but that is only single-thread server. Paste will allow multithread access of users to your server.

Also to change the default database paths, you will need to update :attr:`~storage.settings.ZCONF_PATH` to path with the ZEO configuration.

Example of the configuration
----------------------------

``/etc/edeposit/storage.json``:

.. code-block:: json

    {
        "PUBLIC_DIR": "/var/storage/public",
        "PRIVATE_DIR": "/var/storage/private",
        "ZCONF_PATH": "/var/storage/zconf",
        "PRIVATE_INDEX": true,
        "PRIVATE_INDEX_PASSWORD": "secret password",
        "WEB_SERVER": "paste"
    }

Example of the ZEO configuration
--------------------------------

``/var/storage/zconf/zeo_client.conf``:

.. code-block:: xml

    <zeoclient>
      server localhost:8090
    </zeoclient>

``/var/storage/zconf/zeo.conf``:

.. code-block:: xml

    <zeo>
      address localhost:8090
    </zeo>

    <filestorage>
      path /var/storage/zodb/storage.fs
    </filestorage>

    <eventlog>
      level INFO
      <logfile>
        path /var/storage/zodb/zeo.log
        format %(asctime)s %(message)s
      </logfile>
    </eventlog>


How to run the server
=====================

There are three script, which you have to start in order to get full functionality:

- ``edeposit_storage_runzeo.sh`` (database)
- ``edeposit_storage_server.py`` (webserver)
- ``edeposit_amqp_storaged.py`` (amqp handler)

Webserver and AMQP handler are optional, but database script is mandatory.

Supervisord
-----------

To run the scripts, you can use `supervisord`_:

.. _supervisord: http://supervisord.org

.. code-block:: ini

    [program:storagedaemon]
    command = /usr/bin/edeposit_amqp_storaged.py start --foreground
    process_name = storagedaemon
    directory = /usr/bin
    priority = 10
    redirect_stderr = true
    user = edeposit

    [program:storageweb]
    command = /usr/bin/edeposit_storage_server.py
    process_name = storageweb
    directory = /usr/bin
    priority = 10
    redirect_stderr = true
    user = root

    [program:storagezeo]
    command = /usr/bin/edeposit_storage_runzeo.sh
    process_name = storagezeo
    directory = /usr/bin
    priority = 10
    redirect_stderr = true
    user = edeposit

For the storageweb, the user must be root only in case you wish to run the web on port ``80``.