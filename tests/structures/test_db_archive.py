#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import copy
import uuid
import base64
import random
import os.path
import tempfile

import pytest
from faker import Factory

import storage
from storage.structures.db_archive import Archive
from storage.structures.db_archive import DBArchive

from ..environment_generator import TMP_DIR


# Variables ===================================================================
FAKER = Factory.create('cs_CZ')


# Fixtures ====================================================================
@pytest.fixture
def zip_file():
    fn = os.path.join(os.path.dirname(__file__), "../data/archive.zip")

    with open(fn) as f:
        return f.read()


def b64_zip_file():
    return base64.b64encode(
        zip_file()
    )


@pytest.fixture
def random_archive_comm(monkeypatch):
    monkeypatch.setattr(
        storage.structures.db_archive,
        "ARCHIVE_DIR",
        tempfile.mkdtemp(dir=TMP_DIR)
    )

    return Archive(
        isbn=FAKER.ssn(),
        uuid=str(uuid.uuid4()),
        aleph_id=random.randint(9999, 99999999),
        b64_data=b64_zip_file(),
    )


@pytest.fixture
def random_archive_db(monkeypatch):
    return DBArchive.from_comm(random_archive_comm(monkeypatch))


# Functions & classes =========================================================
def test_random_archive(random_archive_db):
    assert random_archive_db.isbn
    assert random_archive_db.uuid
    assert random_archive_db.aleph_id

    assert random_archive_db.indexes
    assert random_archive_db.project_key

    assert os.path.exists(random_archive_db.dir_pointer)
    assert os.path.isdir(random_archive_db.dir_pointer)

    assert random_archive_db.dir_pointer.startswith("/tmp")

    ra = random_archive_db
    rac = random_archive_db.to_comm()

    assert ra.isbn == rac.isbn
    assert ra.uuid == rac.uuid
    assert ra.aleph_id == rac.aleph_id
    assert ra.dir_pointer == rac.dir_pointer


def test_op_eq(random_archive_db):
    rand_copy = copy.deepcopy(random_archive_db)

    assert random_archive_db == rand_copy
    assert not (random_archive_db != rand_copy)

    rand_copy.isbn = "azgabash"

    assert not (random_archive_db == rand_copy)  # op eq
    assert random_archive_db != rand_copy

    assert random_archive_db != 1


def test_in_operator(monkeypatch):
    ra1 = random_archive_db(monkeypatch)
    ra2 = random_archive_db(monkeypatch)
    ra3 = random_archive_db(monkeypatch)

    assert ra1 != ra2

    cont = set([ra1, ra2])

    assert ra1 in cont
    assert ra2 in cont

    assert ra3 not in cont
