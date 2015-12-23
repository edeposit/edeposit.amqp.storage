#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import transaction
from BTrees.OOBTree import OOSet
from zeo_connector import transaction_manager
from zeo_connector.examples import DatabaseHandler

from settings import ZEO_CLIENT_PATH
from settings import TREE_PROJECT_KEY as PROJECT_KEY


# Variables ===================================================================
_TREE_HANDLER = None


# Functions & classes =========================================================
class TreeHandler(DatabaseHandler):
    """
    This class is used as database handler for :class:`.Tree` instances.

    Attributes:
        name_db_key (str): Key for the :attr:`.name_db`.
        name_db (dict): Database handler dict for `name`.
        aleph_id_db_key (str): Key for the :attr:`.aleph_id_db`.
        aleph_id_db (dict): Database handler dict for `aleph_id`.
        issn_db_key (str): Key for the :attr:`.issn_db`.
        issn_db (dict): Database handler dict for `issn`.
        path_db_key (str): Key for the :attr:`.path_db`.
        path_db (dict): Database handler dict for `path`.
        parent_db_key (str): Key for the :attr:`.parent_db`.
        parent_db (dict): Database handler dict for `parent`.
    """
    def __init__(self, conf_path=ZEO_CLIENT_PATH, project_key=PROJECT_KEY):
        """
        Constructor.

        Args:
            conf_path (str): Path to the ZEO configuration file. Default
                :attr:`~storage.settings.ZEO_CLIENT_PATH`.
            project_key (str): Project key, which is used for lookups into ZEO.
                Default :attr:`~storage.settings.TREE_PROJECT_KEY`.
        """
        super(self.__class__, self).__init__(
            conf_path=conf_path,
            project_key=project_key
        )

        # tree.name -> tree
        self.name_db_key = "name_db"
        self.name_db = self._get_key_or_create(self.name_db_key)

        # tree.aleph_id -> tree
        self.aleph_id_db_key = "aleph_id_db"
        self.aleph_id_db = self._get_key_or_create(self.aleph_id_db_key)

        # tree.issn -> tree
        self.issn_db_key = "issn_db"
        self.issn_db = self._get_key_or_create(self.issn_db_key)

        # tree.path -> tree
        self.path_db_key = "path_db"
        self.path_db = self._get_key_or_create(self.path_db_key)

        # sub_tree.path -> parent
        self.parent_db_key = "parent_db"
        self.parent_db = self._get_key_or_create(self.parent_db_key)

    @transaction_manager
    def _add_to(self, db, index, item, default=OOSet):
        """
        Add `item` to `db` under `index`. If `index` is not yet in `db`, create
        it using `default`.

        Args:
            db (dict-obj): Dict-like object used to connect to database.
            index (str): Index used to look in `db`.
            item (obj): Persistent object, which may be stored in DB.
            default (func/obj): Reference to function/object, which will be
                used to create the object under `index`.
                Default :class:`OOSet`.
        """
        row = db.get(index, None)

        if row is None:
            row = default()
            db[index] = row

        row.add(item)

    @transaction_manager
    def add_tree(self, tree, parent=None):
        """
        Add `tree` into database.

        Args:
            tree (obj): :class:`.Tree` instance.
            parent (ref, default None): Reference to parent tree. This is used
                for all sub-trees in recursive call.
        """
        if tree.path in self.path_db:
            self.remove_tree_by_path(tree.path)

        # index all indexable attributes
        for index in tree.indexes:
            if not getattr(tree, index):
                continue

            self._add_to(
                getattr(self, index + "_db"),
                getattr(tree, index),
                tree,
            )

        if parent:
            self._add_to(self.parent_db, tree.path, parent)

        # make sure, that all sub-trees starts with path of parent tree
        for sub_tree in tree.sub_trees:
            assert sub_tree.path.startswith(tree.path)

        for sub_tree in tree.sub_trees:
            self.add_tree(sub_tree, parent=tree)

    def remove_tree_by_path(self, path):
        """
        Remove the tree from database by given `path`.

        Args:
            path (str): Path of the tree.
        """
        with transaction.manager:
            trees = self.path_db.get(path, None)

        if not trees:
            return

        for tree in trees:
            return self._remove_tree(tree)

    def remove_tree(self, tree):
        """
        Remove the tree from database using `tree` object to identfy the path.

        Args:
            tree (obj): :class:`.Tree` instance.
        """
        return self.remove_tree_by_path(tree.path)

    def _remove_from(self, db, index, item):
        """
        Remove `item` from `db` at `index`.

        Note:
            This function is inverse to :meth:`._add_to`.

        Args:
            db (dict-obj): Dict-like object used to connect to database.
            index (str): Index used to look in `db`.
            item (obj): Persistent object, which may be stored in DB.
        """
        with transaction.manager:
            row = db.get(index, None)

        if row is None:
            return

        with transaction.manager:
            if item in row:
                row.remove(item)

        with transaction.manager:
            if not row:
                del db[index]

    @transaction_manager
    def _remove_tree(self, tree, parent=None):
        """
        Really remove the tree identified by `tree` instance from all indexes
        from database.

        Args:
            tree (obj): :class:`.Tree` instance.
            parent (obj, default None): Reference to parent.
        """
        # remove sub-trees
        for sub_tree in tree.sub_trees:
            self._remove_tree(sub_tree, parent=tree)

        # remove itself
        for index in tree.indexes:
            if not getattr(tree, index):
                continue

            self._remove_from(
                getattr(self, index + "_db"),
                getattr(tree, index),
                tree,
            )

        if parent:
            self._remove_from(self.parent_db, tree.path, parent)

        self.zeo.pack()

    @transaction_manager
    def trees_by_issn(self, issn):
        """
        Search trees by `issn`.

        Args:
            issn (str): :attr:`.Tree.issn` property of :class:`.Tree`.

        Returns:
            set: Set of matching :class:`Tree` instances.
        """
        return set(
            self.issn_db.get(issn, OOSet()).keys()
        )

    @transaction_manager
    def trees_by_path(self, path):
        """
        Search trees by `path`.

        Args:
            path (str): :attr:`.Tree.path` property of :class:`.Tree`.

        Returns:
            set: Set of matching :class:`Tree` instances.
        """
        return set(
            self.path_db.get(path, OOSet()).keys()
        )

    @transaction_manager
    def trees_by_subpath(self, sub_path):
        """
        Search trees by `sub_path` using ``Tree.path.startswith(sub_path)``
        comparison.

        Args:
            sub_path (str): Part of the :attr:`.Tree.path` property of
                :class:`.Tree`.

        Returns:
            set: Set of matching :class:`Tree` instances.
        """
        matches = (
            self.path_db[tree_path].keys()
            for tree_path in self.path_db.iterkeys()
            if tree_path.startswith(sub_path)
        )

        return set(sum(matches, []))  # flattern the list

    @transaction_manager
    def get_parent(self, tree, alt=None):
        """
        Get parent for given `tree` or `alt` if not found.

        Args:
            tree (obj): :class:`.Tree` instance, which is already stored in DB.
            alt (obj, default None): Alternative value returned when `tree` is
                not found.

        Returns:
            obj: :class:`.Tree` parent to given `tree`.
        """
        parent = self.parent_db.get(tree.path)

        if not parent:
            return alt

        return list(parent)[0]


def tree_handler(*args, **kwargs):
    """
    Singleton `TreeHandler` generator. Any arguments are given to
    :class:`TreeHandler`, when it is first created.

    Returns:
        obj: :class:`TreeHandler` instance.
    """
    global _TREE_HANDLER

    if not _TREE_HANDLER:
        _TREE_HANDLER = TreeHandler(*args, **kwargs)

    return _TREE_HANDLER
