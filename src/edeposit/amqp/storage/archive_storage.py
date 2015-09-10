#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from structures import DBArchive

from storage_handler import InvalidType
from storage_handler import store_object
from storage_handler import search_objects

from publication_storage import _assert_obj_type


# Functions & classes =========================================================
def save_archive(archive):
    """
    Save `archive` into database and into proper indexes.

    Attr:
        archive (obj): Instance of the :class:`.DBArchive`.

    Returns:
        obj: :class:`.DBArchive` without data.

    Raises:
        InvalidType: When the `archive` is not instance of :class:`.DBArchive`.
        UnindexablePublication: When there is no index (property) which can be
                                used to index `archive` in database.
    """
    _assert_obj_type(archive, obj_type=DBArchive)

    store_object(archive)

    return archive.to_comm(light_request=True)


def search_archives(query):
    """
    Return list of :class:`.DBArchive` which match all properties that are
    set (``not None``) using AND operator to all of them.

    Example:
        result = storage_handler.search_publications(
            DBArchive(isbn="azgabash")
        )

    Args:
        query (obj): :class:`.DBArchive` with `some` of the properties set.

    Returns:
        list: List of matching :class:`.DBArchive` or ``[]`` if no match \
              was found.

    Raises:
        InvalidType: When the `query` is not instance of :class:`.DBArchive`.
    """
    _assert_obj_type(query, name="query", obj_type=DBArchive)

    return search_objects(query)
