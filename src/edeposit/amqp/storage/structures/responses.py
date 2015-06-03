#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class SearchResult(namedtuple("SearchResult", ["publications"])):
    """
    Response to :class:`.SearchRequest`.

    Attributes:
        publications (list): List of matching :class:`.Publication` objects.
    """
