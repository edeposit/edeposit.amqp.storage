#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOTreeSet, intersection

from zconf import get_zeo_key
from zconf import use_new_connection

from structures import DBPublication
from structures.publication_generator import COMMON_FIELDS


# Exceptions ==================================================================
class InvalidType(Exception):
    pass


class UnindexablePublication(Exception):
    pass


# Functions & classes =========================================================
def _get_db_connectors(cached=True):
    """
    Return list of database dictionaries, which are used as indexes for each
    attributes.

    Args:
        cached (bool, default True): Use cached connection to database.

    Returns:
        list: List of OOBTree's for each item in :attr:`.COMMON_FIELDS`.
    """
    for field_name, docstring in COMMON_FIELDS:
        yield field_name, get_zeo_key(field_name, cached=cached)


def _check_pub_type(pub, name="pub"):
    """
    Make sure, that `pub` is instance of the :class:`.DBPublication`.

    Args:
        pub (obj): Instance which will be checked.
        name (str): Name of the instance. Used in exception.

    Raises:
        InvalidType: When the `pub` is not instance of :class:`.DBPublication`.
    """
    if not isinstance(pub, DBPublication):
        raise InvalidType(
            "`%s` to be instance of DBPublication, not %s!" % (
                name,
                pub.__class__.__name__
            )
        )


def _put_into_indexes(pub):
    """
    Put publication into all indexes.

    Attr:
        pub (obj): Instance of :class:`.DBPublication`.

    Raises:
        UnindexablePublication: When there is no index (property) which can be
                                used to index `pub` in database.
    """
    no_of_used_indexes = 0
    for field_name, db_connector in list(_get_db_connectors()):
        attr = getattr(pub, field_name)

        if attr is None:  # index only by set attributes
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
    """
    Save `pub` into database and into proper indexes.

    Attr:
        pub (obj): Instance of the :class:`.DBPublication`.

    Raises:
        InvalidType: When the `pub` is not instance of :class:`.DBPublication`.
        UnindexablePublication: When there is no index (property) which can be
                                used to index `pub` in database.
    """
    _check_pub_type(pub)

    with transaction.manager:
        _put_into_indexes(pub)


def _get_subset_matches(query):
    """
    Yield publications, at indexes defined by `query` property values.

    Args:
        query (obj): :class:`.DBPublication` with `some` of the properties set.

    Yields:
        list: List of matching publications.
    """
    for field_name, db_connector in _get_db_connectors():
        attr = getattr(query, field_name)

        if attr is None:  # don't use unset attributes
            continue

        results = db_connector.get(attr, [])

        if results:
            yield results


def search_publications(query):
    """
    Return list of :class:`.DBPublication` which match all properties that are
    set (``not None``) using AND operator to all of them.

    Example:
        result = storage_handler.search_publications(
            DBPublication(isbn="azgabash")
        )

    Args:
        query (obj): :class:`.DBPublication` with `some` of the properties set.

    Returns:
        list: List of matching :class:`.DBPublication` or ``[]`` if no match \
              was found.

    Raises:
        InvalidType: When the `query` is not instance of \
                     :class:`.DBPublication`.
    """
    _check_pub_type(query, "query")

    # AND operator between results
    final_result = None
    for result in _get_subset_matches(query):
        if final_result is None:
            final_result = result
            continue

        final_result = intersection(final_result, result)

    # if no result is found, this is None, and I want []
    if not final_result:
        return []

    return list(final_result)
