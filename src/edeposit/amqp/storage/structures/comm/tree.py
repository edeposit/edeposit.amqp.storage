#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions and classes =======================================================
class Tree(namedtuple('Tree', ["name",
                               "sub_trees",
                               "sub_publications",
                               "aleph_id",
                               "issn",
                               "path"])):
    '''
    Communication structure used to sent data to `storage` subsystem over AMQP.

    Attributes:
        name (str): Name of the periodical.
        sub_trees (list): List of other trees.
        sub_publications (list): List of sub-publication UUID's.
        aleph_id (str): ID used in aleph.
        issn (str): ISSN given to the periodical.
        path (str): Path in the periodical structures.
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        assert self.path
        assert type(self.sub_trees) in [list, tuple]
        assert type(self.sub_publications) in [list, tuple]

    @property
    def indexes(self):
        return [
            "name",
            "aleph_id",
            "issn",
            "path",
        ]
