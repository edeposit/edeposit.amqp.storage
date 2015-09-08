#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Object database with indexing by the object attributes.

Each stored object is required to have following properties:

    - indexes (list of strings)
    - project_key (string)

For example::

    class Person(Persistent):
        def __init__(self, name, surname):
            self.name = name
            self.surname = surname

        @property
        def indexes(self):
            return [
                "name",
                "surname",
            ]

        @property
        def project_key(self):
            return PROJECT_KEY

Note:
    I suggest to use properties, because that way the values are not stored in
    database, but constructed at request by the property methods.
"""
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOTreeSet, intersection

from zconf import get_zeo_key
from zconf import use_new_connection


# Exceptions ==================================================================
class InvalidType(Exception):
    pass


class UnindexableObject(Exception):
    pass


# Functions & classes =========================================================
def _get_db_connectors(obj, cached=True):
    """
    Return list of database dictionaries, which are used as indexes for each
    attributes.

    Args:
        cached (bool, default True): Use cached connection to database.

    Returns:
        list: List of OOBTree's for each item in :attr:`.COMMON_FIELDS`.
    """
    pk = obj.project_key
    for field in obj.indexes:
        yield field, get_zeo_key(field, cached=cached, project_key=pk)


def _check_obj_properties(pub, name="pub"):
    """
    Make sure, that `pub` has the right interface.

    Args:
        pub (obj): Instance which will be checked.
        name (str): Name of the instance. Used in exception. Default `pub`.

    Raises:
        InvalidType: When the `pub` is not instance of `obj_type`.
    """
    if not hasattr(pub, "indexes"):
        raise InvalidType("`%s` doesn't have .indexes property!" % name)

    if not pub.indexes:
        raise InvalidType("`%s.indexes` is not set!" % name)

    if not hasattr(pub, "project_key"):
        raise InvalidType("`%s` doesn't have .project_key property!" % name)

    if not pub.project_key:
        raise InvalidType("`%s.project_key` is not set!" % name)


def _put_into_indexes(obj):
    """
    Put publication into all indexes.

    Attr:
        obj (obj): Indexable object.

    Raises:
        UnindexableObject: When there is no index (property) which can be
                                used to index `obj` in database.
    """
    use_new_connection()

    no_of_used_indexes = 0
    for field_name, db_connector in list(_get_db_connectors(obj)):
        attr_value = getattr(obj, field_name)

        if attr_value is None:  # index only by set attributes
            continue

        container = db_connector.get(attr_value, None)
        if container is None:
            container = OOTreeSet()
            db_connector[attr_value] = container

        container.insert(obj)

        no_of_used_indexes += 1

    # make sure that atleast one `attr_value` was used
    if no_of_used_indexes <= 0:
        raise UnindexableObject(
            "You have to use atleast one of the identificators!"
        )


def store_object(obj):
    """
    Save `obj` into database and into proper indexes.

    Attr:
        obj (obj): Indexable object.

    Raises:
        InvalidType: When the `obj` doesn't have right properties.
        Unindexableobjlication: When there is no indexes defined.
    """
    _check_obj_properties(obj)

    with transaction.manager:
        _put_into_indexes(obj)


def _get_subset_matches(query):
    """
    Yield publications, at indexes defined by `query` property values.

    Args:
        query (obj): Object implementing proper interface.

    Yields:
        list: List of matching publications.
    """
    for field_name, db_connector in _get_db_connectors(query):
        attr = getattr(query, field_name)

        if attr is None:  # don't use unset attributes
            continue

        results = db_connector.get(attr, OOTreeSet())

        if results:
            yield results


def search_objects(query):
    """
    Return list of objects which match all properties that are set
    (``not None``) using AND operator to all of them.

    Example:
        result = storage_handler.search_objects(
            DBPublication(isbn="azgabash")
        )

    Args:
        query (obj): Object implementing proper interface with some of the
              properties set.

    Returns:
        list: List of matching objects or ``[]`` if no match was found.

    Raises:
        InvalidType: When the `query` doesn't implement required properties.
    """
    _check_obj_properties(query, "query")

    # AND operator between results
    final_result = None
    for result in _get_subset_matches(query):
        if final_result is None:
            final_result = result
            continue

        final_result = intersection(final_result, result)

    # if no result is found, `final_result` is None, and I want []
    if not final_result:
        return []

    return list(final_result)
