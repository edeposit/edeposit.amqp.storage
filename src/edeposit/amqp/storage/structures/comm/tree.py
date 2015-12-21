#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path
from collections import namedtuple


# Functions and classes =======================================================
class Tree(namedtuple('Tree', ["name",
                               "sub_trees",
                               "sub_publications",
                               "aleph_id",
                               "issn",
                               "path_array"])):
    '''
    Communication structure used to sent data to `storage` subsystem over AMQP.

    Attributes:
        name (str): Name of the periodical.
        sub_trees (list): List of other trees.
        sub_publications (list): List of sub-publication UUID's.
        aleph_id (str): ID used in aleph.
        issn (str): ISSN given to the periodical.
        path (str, default ""): Path in the periodical structures.
    '''

    def __new__(self, *args, **kwargs):
        """
        This hack is here to allow specyfing the optional `path` argument,
        which is then saved into mutable property path_array.
        """
        path = None
        if len(args) == 6:
            path = args[-1]
            args = args[:5]

        if "path" in kwargs:
            path = kwargs["path"]
            del kwargs["path"]

        if "path_array" not in kwargs:
            kwargs["path_array"] = ["" if path is None else path]

        return super(Tree, self).__new__(self, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        assert type(self.sub_trees) in [list, tuple]
        assert type(self.sub_publications) in [list, tuple]

        if not self.path:
            self.path = self.name

        for sub_tree in self.sub_trees:
            sub_tree.path = os.path.join(self.path, sub_tree.name)

    @property
    def path(self):
        return self.path_array[0]

    @path.setter
    def path(self, val):
        self.path_array[0] = val

    @property
    def indexes(self):
        return [
            "name",
            "aleph_id",
            "issn",
            "path"
        ]
