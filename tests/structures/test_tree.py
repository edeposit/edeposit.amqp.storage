#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from storage.structures import Tree


# Tests =======================================================================
def test_Tree():
    t = Tree(
        name="2015",
        sub_trees=[],
        sub_publications=["first", "second"],
        aleph_id=None,
        issn=None,
        # path="Mladá fronta/2015",
    )

    assert t.name == "2015"
    assert t.sub_trees == []
    assert t.sub_publications == ["first", "second"]
    assert t.aleph_id is None
    assert t.issn is None
    assert t.path == ""


def test_Tree_set_path():
    t = Tree(
        name="2015",
        sub_trees=[],
        sub_publications=["first", "second"],
        aleph_id=None,
        issn=None,
        path="Mladá fronta",
    )

    assert t.name == "2015"
    assert t.sub_trees == []
    assert t.sub_publications == ["first", "second"]
    assert t.aleph_id is None
    assert t.issn is None
    assert t.path == "Mladá fronta"

    t.path = "xe"
    assert t.path == "xe"


def test_Tree_set_path_array():
    t = Tree(
        name="2015",
        sub_trees=[],
        sub_publications=["first", "second"],
        aleph_id=None,
        issn=None,
        path_array=["Mladá fronta"],
    )

    assert t.name == "2015"
    assert t.sub_trees == []
    assert t.sub_publications == ["first", "second"]
    assert t.aleph_id is None
    assert t.issn is None
    assert t.path == "Mladá fronta"
