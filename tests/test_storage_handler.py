#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import os
import copy
import shutil
import os.path
import tempfile
import subprocess
from string import Template
from multiprocessing import Process

import pytest

import storage
from storage import zconf
from storage import settings
from storage import storage_handler
from storage.structures import DBPublication

from structures.test_db_publication import random_publication


# Variables ===================================================================
TMP_DIR = None
SERV = None
FULL_PUB = random_publication()


# Fixtures ====================================================================
def data_context(fn, mode="r"):
    path = os.path.join(os.path.dirname(__file__), "data")

    with open(os.path.join(path, fn), mode) as f:
        return f.read()


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
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()

    # monkey patch the paths
    settings.ZCONF_PATH = TMP_DIR
    zconf.ZCONF_PATH = TMP_DIR

    # write ZEO server config to  temp directory
    zeo_conf_path = os.path.join(TMP_DIR, "zeo.conf")
    with open(zeo_conf_path, "w") as f:
        f.write(
            Template(data_context("zeo.conf")).substitute(path=TMP_DIR)
        )

    # write client config to temp directory
    client_config_path = os.path.join(TMP_DIR, "zeo_client.conf")
    with open(client_config_path, "w") as f:
        f.write(data_context("zeo_client.conf"))

    # run the ZEO server
    def run_zeo():
        # subprocess.check_call("runzeo -C " + zeo_conf_path, shell=True)
        import sh  # TODO: remove
        sh.runzeo(C=zeo_conf_path)

    global SERV
    SERV = Process(target=run_zeo)
    SERV.start()


def teardown_module(module):
    SERV.terminate()
    shutil.rmtree(TMP_DIR)


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
