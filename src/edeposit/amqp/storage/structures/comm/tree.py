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
    @property
    def indexes(self):
        return [
            "name",
            "aleph_id",
            "issn",
            "path",
        ]
