#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
import shutil
import tempfile
from string import Template

import pytest

from storage import settings


# Variables ===================================================================
TMP_DIR = None


# Fixtures ====================================================================
def data_context(fn):
    path = os.path.join(os.path.dirname(__file__), "data")

    with open(os.path.join(path, fn)) as f:
        return f.read()

# @pytest.fixture
# def fixture():
#     pass

# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def setup_module(module):
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()

    with open(os.path.join(TMP_DIR, "zeo.conf"), "w") as f:
        f.write(
            Template(data_context("zeo.conf")).substitute(
                path=TMP_DIR
            )
        )

    with open(os.path.join(TMP_DIR, "zeo_client.conf"), "w") as f:
        f.write(data_context("zeo_client.conf"))


def test_get_db_connectors():
    pass


def test_check_pub_type():
    pass


def teardown_module(module):
    shutil.rmtree(TMP_DIR)
