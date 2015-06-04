#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction

import settings
from zconf import get_zeo_key

from structures import DBPublication
from structures.publication_generator import COMMON_FIELDS


# Variables ===================================================================
# Functions & classes =========================================================
def _get_db_connectors():
    for field_name, docstring in COMMON_FIELDS:
        if "(bool" in docstring:
            continue

        yield field_name, get_zeo_key(field_name)


def save_publication(pub):
    error_msg = "`pub` to be instance of DBPublication, not %s!"
    assert isinstance(pub, DBPublication), error_msg % pub.__class__.__name__

    for field_name, db_connector in _get_db_connectors():
        index = getattr(pub, field_name)

        if not index:
            continue

        db_connector[index] = db_connector.get(index, []) + [pub]

    transaction.commit()


def search_publications(query):
    db = get_zeo_key("")
