#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOTreeSet, intersection


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


def _index_publication(pub):
    no_of_used_indexes = 0
    for field_name, db_connector in list(_get_db_connectors()):
        attr = getattr(pub, field_name)

        if not attr:  # index only by set attributes
            continue

        handler = db_connector.get(attr, OOTreeSet())
        handler.insert(pub)
        db_connector[attr] = handler

        no_of_used_indexes += 1

    # make sure that atleast one attr was used
    if no_of_used_indexes <= 0:
        raise UnindexablePublication(
            "You have to use atleast one of the identificators!"
        )


def save_publication(pub):
    _check_pub_type(pub)

    with transaction.manager:
        # put publication into all indexes
        _index_publication(pub)

        # save to list of public/private publications
        list_db = get_zeo_key(
            PUB_KEY if pub.is_public else PRIV_KEY,
            OOTreeSet
        )
        list_db.insert(pub)


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

        final_result = intersection(final_result, result)

    return final_result
