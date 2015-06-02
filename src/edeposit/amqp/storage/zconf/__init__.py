#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

import ZODB.config
from ZODB import DB
from BTrees.OOBTree import OOBTree

from ..settings import ZCONF_PATH
from ..settings import PROJECT_KEY


# Functions & classes =========================================================
def get_zeo_connection():
    path = os.path.join(ZCONF_PATH, "zeo_client.conf")
    db = DB(
        ZODB.config.storageFromFile(open(path))
    )
    return db.open()


def get_zeo_root():
    conn = get_zeo_connection()
    dbroot = conn.root()

    if PROJECT_KEY not in dbroot:
        from BTrees.OOBTree import OOBTree
        dbroot[PROJECT_KEY] = OOBTree()

    return dbroot[PROJECT_KEY]


def get_zeo_key(key, new_obj=OOBTree):
    root = get_zeo_root()

    if not root.get(key, None):
        root[key] = new_obj()

    return root[key]
