#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

from ZODB import DB
from ZODB.config import storageFromFile
from ZODB.POSException import ConnectionStateError

from BTrees.OOBTree import OOBTree

from ..settings import ZCONF_PATH
from ..settings import PROJECT_KEY


# Variables ===================================================================
_ROOT = None


# Functions & classes =========================================================
def get_zeo_connection(on_close_callback=None):
    path = os.path.join(ZCONF_PATH, "zeo_client.conf")
    db = DB(storageFromFile(open(path)))
    connection = db.open()

    if on_close_callback:
        connection.onCloseCallback(on_close_callback)

    return connection


def get_zeo_root(cached=True):
    global _ROOT
    if _ROOT and cached:
        return _ROOT

    def unset_root_cache():
        global _ROOT
        _ROOT = None

    connection = get_zeo_connection(on_close_callback=unset_root_cache)

    try:
        dbroot = connection.root()
    except ConnectionStateError:
        return get_zeo_root(cached=False)

    if PROJECT_KEY not in dbroot:
        dbroot[PROJECT_KEY] = OOBTree()

    _ROOT = dbroot[PROJECT_KEY]
    return _ROOT


def get_zeo_key(key, new_type=OOBTree):
    root = get_zeo_root()

    if not root.get(key, None):
        root[key] = new_type()

    return root[key]
