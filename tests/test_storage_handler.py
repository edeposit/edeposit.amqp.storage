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

# for fixture - pytest bug
from structures.test_db_publication import random_publication
from structures.test_db_publication import random_publication_comm

from test_publication_storage import full_publication


# Setup =======================================================================
def setup_module(module):
    environment_generator.generate_environment()


def teardown_module(module):
    environment_generator.cleanup_environment()


# Tests =======================================================================
def test_get_db_connectors(full_publication):
    connectors = storage_handler._get_db_connectors(full_publication)

    assert len(list(connectors)) > 1
