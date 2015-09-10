edeposit.amqp.storage
=====================

Long term storage subsystem for the E-deposit_ project.

This project allows to store and retreive publications over AMQP_ and also to optionally access accessible publications via HTTP using builtin webserver written in bottle.py_.

.. _AMQP: https://www.amqp.org/
.. _bottle.py: http://bottlepy.org
.. _E-deposit: http://edeposit.nkp.cz/

Package structure
-----------------

File relations
++++++++++++++

.. image:: /_static/relations.png
    :width: 400px

API
+++

:doc:`/api/storage`:

.. toctree::
    :maxdepth: 1

    /api/archive_storage.rst
    /api/publication_storage.rst

.. toctree::
    :maxdepth: 1

    /api/api.rst
    /api/storage_handler.rst
    /api/web_tools.rst
    /api/zconf.rst
    /api/settings.rst

:doc:`/api/structures/structures`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AMQP:

.. toctree::
    :maxdepth: 1

    /api/structures/responses.rst
    /api/structures/requests.rst

.. toctree::
    :maxdepth: 1

    /api/structures/publication.rst
    /api/structures/archive.rst

Database:

.. toctree::
    :maxdepth: 1

    /api/structures/db_publication.rst
    /api/structures/db_archive.rst

.. toctree::
    :maxdepth: 1

Generators:

.. toctree::
    :maxdepth: 1

    /api/structures/structures_generator.rst

Installation
------------

Installation of this project is little bit more complicated. Please read installation notes:

.. toctree::
    :maxdepth: 1

    /installation/installation_notes.rst

Source code
+++++++++++
Project is released under the MIT license. Source code can be found at GitHub:

- https://github.com/edeposit/edeposit.amqp.storage

Unittests
+++++++++

Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

If you have any trouble, just add ``--pdb`` switch at the end of your ``run_tests.sh`` command like this: ``./run_tests.sh --pdb``. This will drop you to `PDB`_ shell.

.. _PDB: https://docs.python.org/2/library/pdb.html

Requirements
^^^^^^^^^^^^
This script expects that packages pytest_, fake-factory_ and sh_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest fake-factory sh

or for all users::

    sudo pip install pytest fake-factory sh

.. _pytest: http://pytest.org/
.. _fake-factory: https://github.com/joke2k/faker
.. _sh: https://github.com/amoffat/sh


Example
^^^^^^^
::

    ./run_tests.sh 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.26 -- pytest-2.6.4
    plugins: cov
    collected 15 items 

    tests/test_amqp_chain.py ..
    tests/test_storage_handler.py .........
    tests/structures/test_db_publication.py ...
    tests/structures/test_publication.py .

    ========================== 15 passed in 11.20 seconds ==========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
