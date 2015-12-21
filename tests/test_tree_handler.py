#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from storage.structures import Tree
from storage.tree_handler import TreeHandler

from structures.test_tree import sample_tree


# Variables ===================================================================
# Fixtures ====================================================================
@pytest.fixture(scope="module", autouse=True)
def tree_handler(client_conf_path):
    return TreeHandler(conf_path=client_conf_path)


# Tests =======================================================================
def test_tree(sample_tree):
    assert sample_tree


def test_tree_handler_add_tree(sample_tree, tree_handler):
    tree_handler.add_tree(sample_tree)

    assert sample_tree in tree_handler.name_db[sample_tree.name]
    assert sample_tree in tree_handler.aleph_id_db[sample_tree.aleph_id]
    assert sample_tree in tree_handler.issn_db[sample_tree.issn]
    assert sample_tree in tree_handler.path_db[sample_tree.path]
    assert sample_tree.path not in tree_handler.parent_db

    first_subtree = sample_tree.sub_trees[0]
    second_subtree = sample_tree.sub_trees[1]

    assert first_subtree in tree_handler.name_db[first_subtree.name]
    # assert first_subtree.aleph_id not in tree_handler.aleph_id_db
    # assert first_subtree.issn not in tree_handler.issn_db
    assert first_subtree in tree_handler.path_db[first_subtree.path]
    assert sample_tree in tree_handler.parent_db[first_subtree.path]

    assert second_subtree in tree_handler.name_db[second_subtree.name]
    # assert second_subtree.aleph_id not in tree_handler.aleph_id_db
    # assert second_subtree.issn not in tree_handler.issn_db
    assert second_subtree in tree_handler.path_db[second_subtree.path]
    assert sample_tree in tree_handler.parent_db[second_subtree.path]


def test_tree_handler_remove_tree(sample_tree, tree_handler):
    tree_handler.remove_tree(sample_tree)

    assert sample_tree.name not in tree_handler.name_db
    assert sample_tree.aleph_id not in tree_handler.aleph_id_db
    assert sample_tree.issn not in tree_handler.issn_db
    assert sample_tree.path not in tree_handler.path_db
    assert sample_tree.path not in tree_handler.parent_db

    first_subtree = sample_tree.sub_trees[0]
    second_subtree = sample_tree.sub_trees[1]

    assert first_subtree.name not in tree_handler.name_db
    # assert first_subtree.aleph_id not in tree_handler.aleph_id_db
    # assert first_subtree.issn not in tree_handler.issn_db
    assert first_subtree.path not in tree_handler.path_db

    assert second_subtree.name not in tree_handler.name_db
    # assert second_subtree.aleph_id not in tree_handler.aleph_id_db
    # assert second_subtree.issn not in tree_handler.issn_db
    assert second_subtree.path not in tree_handler.path_db

    assert not tree_handler.name_db
    assert not tree_handler.aleph_id_db
    assert not tree_handler.issn_db
    assert not tree_handler.path_db
    assert not tree_handler.parent_db


def test_tree_handler_tree_by_issn(sample_tree, tree_handler):
    tree_handler.add_tree(sample_tree)

    trees = tree_handler.trees_by_issn(sample_tree.issn)

    assert trees == set([sample_tree])


def test_trees_by_path(sample_tree, tree_handler):
    trees = tree_handler.trees_by_path(sample_tree.path)

    assert trees == set([sample_tree])


def test_subtrees_by_path(sample_tree, tree_handler):
    sub_tree = tree_handler.trees_by_path(sample_tree.sub_trees[0].path)

    assert sub_tree == set([sample_tree.sub_trees[0]])


def test_trees_by_subpath(sample_tree, tree_handler):
    trees = tree_handler.trees_by_subpath(sample_tree.path + "/20")

    assert trees == set(sample_tree.sub_trees)


def test_get_parent(sample_tree, tree_handler):
    parent = tree_handler.get_parent(sample_tree.sub_trees[0])

    assert parent == sample_tree
