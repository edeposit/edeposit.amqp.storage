#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from storage import Publication


# Tests =======================================================================
def test_publication_creation():
    pub = Publication(title="azgabash")  # create with only one element

    assert pub.title == "azgabash"
    assert pub.author is None
