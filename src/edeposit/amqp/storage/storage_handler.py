#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOBTree
from BTrees.OOBTree import OOTreeSet
from BTrees.OOBTree import intersection

from zeo_connector import transaction_manager
from zeo_connector.examples import DatabaseHandler

import settings


# Exceptions ==================================================================
class InvalidType(Exception):
    """
    Raised in case that object you are trying to store doesn't have required
    interface.
    """


class UnindexableObject(Exception):
    """
    Raised in case, that object doesn't have at least one attribute set.
    """


# Functions & classes =========================================================
class StorageHandler(DatabaseHandler):
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
        I suggest to use properties, because that way the values are not stored
        in database, but constructed at request by the property methods.
    """
    def __init__(self, project_key, conf_path=settings.ZEO_CLIENT_PATH):
        """
        Constructor.

        Args:
            project_key (str): Project key which is used for the root of DB.
            conf_path (str): Path to the client zeo configuration file. Default
                :attr:`.settings.ZEO_CLIENT_PATH`.
        """
        super(self.__class__, self).__init__(
            conf_path=conf_path,
            project_key=project_key
        )

    @transaction_manager
    def _zeo_key(self, key, new_type=OOBTree):
        """
        Get key from the :attr:`zeo` database root. If the key doesn't exist,
        create it by calling `new_type` argument.

        Args:
            key (str): Key in the root dict.
            new_type (func/obj): Object/function returning the new instance.

        Returns:
            obj: Stored object, or `new_type`.
        """
        zeo_key = self.zeo.get(key, None)

        if zeo_key is None:
            zeo_key = new_type()
            self.zeo[key] = zeo_key

        return zeo_key

    def _get_db_fields(self, obj):
        """
        Return list of database dictionaries, which are used as indexes for
        each attributes.

        Args:
            cached (bool, default True): Use cached connection to database.

        Returns:
            list: List of OOBTree's for each item in :attr:`.COMMON_FIELDS`.
        """
        for field in obj.indexes:
            yield field, self._zeo_key(field)

    def _check_obj_properties(self, pub, name="pub"):
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
            raise InvalidType(
                "`%s` doesn't have .project_key property!" % name
            )

        if not pub.project_key:
            raise InvalidType("`%s.project_key` is not set!" % name)

    def _put_into_indexes(self, obj):
        """
        Put publication into all indexes.

        Attr:
            obj (obj): Indexable object.

        Raises:
            UnindexableObject: When there is no index (property) which can be
                used to index `obj` in database.
        """
        no_of_used_indexes = 0
        for field_name, db_index in list(self._get_db_fields(obj)):
            attr_value = getattr(obj, field_name)

            if attr_value is None:  # index only by set attributes
                continue

            container = db_index.get(attr_value, None)
            if container is None:
                container = OOTreeSet()
                db_index[attr_value] = container

            container.insert(obj)

            no_of_used_indexes += 1

        # make sure that atleast one `attr_value` was used
        if no_of_used_indexes <= 0:
            raise UnindexableObject(
                "You have to use atleast one of the identificators!"
            )

    def store_object(self, obj):
        """
        Save `obj` into database and into proper indexes.

        Attr:
            obj (obj): Indexable object.

        Raises:
            InvalidType: When the `obj` doesn't have right properties.
            Unindexableobjlication: When there is no indexes defined.
        """
        self._check_obj_properties(obj)

        with transaction.manager:
            self._put_into_indexes(obj)

    def _get_subset_matches(self, query):
        """
        Yield publications, at indexes defined by `query` property values.

        Args:
            query (obj): Object implementing proper interface.

        Yields:
            list: List of matching publications.
        """
        for field_name, db_index in self._get_db_fields(query):
            attr = getattr(query, field_name)

            if attr is None:  # don't use unset attributes
                continue

            results = db_index.get(attr, OOTreeSet())

            if results:
                yield results

    def search_objects(self, query):
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
            InvalidType: When the `query` doesn't implement required
                properties.
        """
        self._check_obj_properties(query, "query")

        # AND operator between results
        final_result = None
        for result in self._get_subset_matches(query):
            if final_result is None:
                final_result = result
                continue

            final_result = intersection(final_result, result)

        # if no result is found, `final_result` is None, and I want []
        if not final_result:
            return []

        return list(final_result)
