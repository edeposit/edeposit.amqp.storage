#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from storage.structures import Tree


# Fixtures ====================================================================
@pytest.fixture
def sample_tree():
    return Tree(
        name="Mladá fronta",
        sub_trees=[
            Tree(
                name="2015",
                sub_trees=[],
                sub_publications=[
                    "first",
                    "second"
                ],
                aleph_id=None,
                issn=None,
            ),
            Tree(
                name="2014",
                sub_trees=[],
                sub_publications=[
                    "first",
                    "second"
                ],
                aleph_id=None,
                issn=None,
            ),
        ],
        sub_publications=[
        ],
        aleph_id="0005389",
        issn="1805-8787",
    )


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
    assert t.path == "2015"


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


def test_sample_tree(sample_tree):
    assert sample_tree.path == "Mladá fronta"
    assert sample_tree.sub_trees[0].path == "Mladá fronta/2015"
    assert sample_tree.sub_trees[1].path == "Mladá fronta/2014"
