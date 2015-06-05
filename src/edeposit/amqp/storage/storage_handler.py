#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOSet


import settings
from zconf import get_zeo_key

from structures import DBPublication
from structures.publication_generator import COMMON_FIELDS


# Variables ===================================================================
PUB_KEY = "public"
PRIV_KEY = "private"


# Exceptions ==================================================================
class InvalidType(Exception):
    pass


class UnindexablePublication(Exception):
    pass


# Functions & classes =========================================================
def _get_db_connectors():
    for field_name, docstring in COMMON_FIELDS:
        if "(bool" in docstring:
            continue

        yield field_name, get_zeo_key(field_name)


def _check_pub_type(pub, name="pub"):
    if not isinstance(pub, DBPublication):
        raise InvalidType(
            "`%s` to be instance of DBPublication, not %s!" % (
                name,
                pub.__class__.__name__
            )
        )


def save_publication(pub):
    _check_pub_type(pub)

    no_of_used_indexes = 0
    for field_name, db_connector in _get_db_connectors():
        attr = getattr(pub, field_name)

        if not attr:
            continue

        db_connector[attr] = db_connector.get(attr, []) + [pub]
        no_of_used_indexes += 1

    # make sure that atleast one attr was used
    if no_of_used_indexes <= 0:
        transaction.abort()
        raise UnindexablePublication(
            "You have to use atleast one of the identificators!"
        )

    # save to list of public/private publications
    key_type = PUB_KEY if pub.is_public else PRIV_KEY
    list_db = get_zeo_key(key_type, OOSet)
    list_db.insert(pub)

    transaction.commit()


def _get_subset_matches(query):
    for field_name, db_connector in _get_db_connectors():
        attr = getattr(query, field_name)

        if not attr:
            continue

        results = db_connector.get(attr, [])

        if results:
            yield set(results)


def search_publications(query):
    _check_pub_type(query, "query")

    # AND operator between results
    final_result = None
    for result in _get_subset_matches(query):
        if final_result is None:
            final_result = result
            continue

        final_result = final_result.intersection(result)

    return final_result
