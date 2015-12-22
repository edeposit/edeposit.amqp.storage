#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class SearchResult(namedtuple("SearchResult", ["records"])):
    """
    Response to :class:`.SearchRequest`.

    Attributes:
        records (list): List of matching :class:`.Publication` objects.
    """


class TreeInfo(namedtuple("TreeInfo", "path url_by_path url_by_issn")):
    """
    Informations about stored trees.

    Attributes:
        path (str): Path of the tree in storage.
        url_by_path (str): Full url-encoded path of the tree in storage.
        url_by_issn (str): URL composed from ISSN.
    """
