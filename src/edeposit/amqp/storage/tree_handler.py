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
# Functions & classes =========================================================
class InvalidSubtreeError(IndexError):
    """
    Raised in case, that sub-tree starts with different path than parent.
    """


class TreeHandler(DatabaseHandler):
    def __init__(self, conf_path=ZEO_CLIENT_PATH, project_key=PROJECT_KEY):
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
        row = db.get(index, None)

        if row is None:
            row = default()
            db[index] = row

        row.add(item)

    @transaction_manager
    def add_tree(self, tree, parent=None):
        if tree.path in self.path_db:
            self.remove_tree(tree.path)

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

    def _remove_from(self, db, index, item):
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

    def remove_tree_by_path(self, path):
        trees = self.path_db.get(path, None)

        if not trees:
            return

        for tree in trees:
            return self._remove_tree(tree)

    def remove_tree(self, tree):
        return self.remove_tree_by_path(tree.path)

    def _remove_tree(self, tree):
        # remove sub-trees
        for sub_tree in tree.sub_trees:
            self._remove_tree(sub_tree)

        # remove itself
        for index in tree.indexes:
            if not getattr(tree, index):
                continue

            self._remove_from(
                getattr(self, index + "_db"),
                getattr(tree, index),
                tree,
            )

        self._remove_from(self.parent_db, tree.path, tree)
