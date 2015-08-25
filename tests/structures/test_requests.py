#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from storage import Publication
from storage.structures import SearchRequest


# Fixtures ====================================================================
@pytest.fixture
def publication():
    return Publication(title="azgabash")


# Tests =======================================================================
def test_SearchRequest(publication):
    with pytest.raises(AssertionError):
        SearchRequest("hello")

    with pytest.raises(AssertionError):
        SearchRequest("hello", True)

    with pytest.raises(AssertionError):
        SearchRequest("hello", False)

    sr = SearchRequest(publication)
    assert sr.query == publication
    assert not sr.light_request

    sr = SearchRequest(publication, True)
    assert sr.query == publication
    assert sr.light_request
