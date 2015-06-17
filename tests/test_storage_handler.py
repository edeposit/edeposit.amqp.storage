#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import copy

import pytest

import storage
from storage import zconf
from storage import settings
from storage import storage_handler
from storage.structures import DBPublication

import environment_generator
from structures.test_db_publication import random_publication


# Variables ===================================================================
FULL_PUB = random_publication()


# Fixtures ====================================================================
@pytest.fixture
def full_publication():
    return FULL_PUB


@pytest.fixture
def different_pub():
    dp = copy.deepcopy(full_publication())
    dp.title = "other title"
    dp.author = "other author"
    dp.is_public = False

    return dp


# Setup =======================================================================
def setup_module(module):
    environment_generator.generate_environment()


def teardown_module(module):
    environment_generator.cleanup_environment()


# Tests =======================================================================
def test_get_db_connectors():
    connectors = storage_handler._get_db_connectors()

    assert len(list(connectors)) > 1


def test_check_pub_type():
    with pytest.raises(storage_handler.InvalidType):
        storage_handler._check_pub_type(object)

    with pytest.raises(storage_handler.InvalidType):
        storage_handler._check_pub_type(
            storage.structures.publication.Publication(*range(11))
        )

    storage_handler._check_pub_type(DBPublication())


def test_save_publication(full_publication):
    storage_handler.save_publication(full_publication)


def test_search_publication(full_publication):
    result = storage_handler.search_publications(full_publication)

    assert result
    assert result[0] == full_publication


def test_search_multiple_publications(full_publication, different_pub):
    storage_handler.save_publication(different_pub)

    result = storage_handler.search_publications(
        DBPublication(title=different_pub.title)
    )

    assert result
    assert len(result) == 1
    assert result[0] == different_pub


def test_result_multiple_publications(full_publication, different_pub):
    result = storage_handler.search_publications(
        DBPublication(isbn=different_pub.isbn)  # ISBN should be same
    )

    assert result
    assert len(result) == 2
    assert set(result) == set([full_publication, different_pub])


def test_no_result_from_query(full_publication, different_pub):
    result = storage_handler.search_publications(
        DBPublication(isbn="azgabash")  # this isbn is not in database
    )

    assert not result


def test_get_public_publications(full_publication):
    result = storage_handler.search_publications(
        DBPublication(is_public=True)
    )

    assert result
    assert set(result) == set([full_publication])


def test_get_private_publications(different_pub):
    result = storage_handler.search_publications(
        DBPublication(is_public=False)
    )

    assert result
    assert set(result) == set([different_pub])
