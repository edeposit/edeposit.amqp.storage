#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from structures import DBPublication

from storage_handler import InvalidType
from storage_handler import StorageHandler

import settings


# Variables ===================================================================
_STORAGE_HANDLER = None


# Functions & classes =========================================================
def _get_handler():
    global _STORAGE_HANDLER

    if _STORAGE_HANDLER is None:
        _STORAGE_HANDLER = StorageHandler(settings.PUB_PROJECT_KEY)

    return _STORAGE_HANDLER


def _assert_obj_type(pub, name="pub", obj_type=DBPublication):
    """
    Make sure, that `pub` is instance of the `obj_type`.

    Args:
        pub (obj): Instance which will be checked.
        name (str): Name of the instance. Used in exception. Default `pub`.
        obj_type (class): Class of which the `pub` should be instance. Default
                 :class:`.DBPublication`.

    Raises:
        InvalidType: When the `pub` is not instance of `obj_type`.
    """
    if not isinstance(pub, obj_type):
        raise InvalidType(
            "`%s` have to be instance of %s, not %s!" % (
                name,
                obj_type.__name__,
                pub.__class__.__name__
            )
        )


def save_publication(pub):
    """
    Save `pub` into database and into proper indexes.

    Attr:
        pub (obj): Instance of the :class:`.DBPublication`.

    Returns:
        obj: :class:`.DBPublication` without data.

    Raises:
        InvalidType: When the `pub` is not instance of :class:`.DBPublication`.
        UnindexablePublication: When there is no index (property) which can be
                                used to index `pub` in database.
    """
    _assert_obj_type(pub)

    _get_handler().store_object(pub)

    return pub.to_comm(light_request=True)


def search_pubs_by_uuid(uuid):
    """
    Search publications by `uuid`.

    Args:
        uuid (str): UUID of publication.

    Returns:
        list: List of matching :class:`.DBPublication` or ``[]`` if no match \
              was found.
    """
    with transaction.manager:
        return list(_get_handler()._zeo_key("uuid").get(uuid, []))


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
    _assert_obj_type(query, "query")

    return _get_handler().search_objects(query)
