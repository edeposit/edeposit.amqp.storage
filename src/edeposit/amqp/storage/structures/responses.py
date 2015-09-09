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
