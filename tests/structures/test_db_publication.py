#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import uuid
import copy
import base64
import random
import os.path
import tempfile

from BTrees.OOBTree import OOTreeSet

import pytest
from faker import Factory

import storage
from storage.structures.db_publication import Publication
from storage.structures.db_publication import DBPublication

from ..environment_generator import TMP_DIR


# Variables ===================================================================
FAKER = Factory.create('cs_CZ')


# Fixtures ====================================================================
@pytest.fixture
def pdf_file():
    fn = os.path.join(os.path.dirname(__file__), "../data/ebook.pdf")

    with open(fn) as f:
        return f.read()


@pytest.fixture
def b64_pdf_file():
    return base64.b64encode(
        pdf_file()
    )


@pytest.fixture
def random_publication_comm(monkeypatch):
    monkeypatch.setattr(
        storage.structures.db_publication,
        "PUBLIC_DIR",
        tempfile.mkdtemp(dir=TMP_DIR)
    )
    monkeypatch.setattr(
        storage.structures.db_publication,
        "PRIVATE_DIR",
        tempfile.mkdtemp(dir=TMP_DIR)
    )

    return Publication(
        title=FAKER.text(20),
        author=FAKER.name(),
        pub_year="%04d" % random.randint(1990, 2015),
        isbn=FAKER.ssn(),
        urnnbn="urn:nbn:cz:edep002-00%04d" % random.randint(0, 999),
        uuid=str(uuid.uuid4()),
        is_public=True,
        b64_data=b64_pdf_file(),
        filename="/home/xex.pdf",
    )


@pytest.fixture
def random_publication(monkeypatch):
    return DBPublication.from_comm(random_publication_comm(monkeypatch))


# Tests =======================================================================
def test_random_publication(random_publication):
    assert random_publication.title
    assert random_publication.author
    assert random_publication.pub_year
    assert random_publication.isbn
    assert random_publication.urnnbn
    assert random_publication.uuid
    assert random_publication.is_public
    assert random_publication.filename

    assert random_publication.indexes
    assert random_publication.project_key

    assert os.path.exists(random_publication.file_pointer)
    assert os.path.isfile(random_publication.file_pointer)

    assert random_publication.file_pointer.startswith("/tmp")

    rp = random_publication
    rpc = random_publication.to_comm()

    assert rp.title == rpc.title
    assert rp.author == rpc.author
    assert rp.pub_year == rpc.pub_year
    assert rp.isbn == rpc.isbn
    assert rp.urnnbn == rpc.urnnbn
    assert rp.uuid == rpc.uuid
    assert rp.is_public == rpc.is_public
    assert rp.filename == rpc.filename
    assert rp.file_pointer == rpc.file_pointer


def test_op_eq(random_publication):
    rand_copy = copy.deepcopy(random_publication)

    assert random_publication == rand_copy
    # assert random_publication.__hash__() == rand_copy.__hash__()
    assert not (random_publication != rand_copy)

    rand_copy.title = "azgabash"

    assert not (random_publication == rand_copy)  # op eq
    # assert random_publication.__hash__() != rand_copy.__hash__()
    assert random_publication != rand_copy

    assert random_publication != 1


def test_in_operator(monkeypatch):
    rp1 = random_publication(monkeypatch)
    rp2 = random_publication(monkeypatch)
    rp3 = random_publication(monkeypatch)

    assert rp1 != rp2

    cont = set([rp1, rp2])

    assert rp1 in cont
    assert rp2 in cont

    assert rp3 not in cont


def test_OOTreeSet(monkeypatch):
    a = OOTreeSet()
    rp1 = random_publication(monkeypatch)
    rp2 = random_publication(monkeypatch)
    rp3 = random_publication(monkeypatch)

    a.insert(rp1)

    assert rp1 in a
    assert rp2 not in a
    assert rp3 not in a
    assert not (rp2 in a)
    assert not (rp3 in a)

    a.insert(rp2)
    assert len(a) == 2

    assert rp1 in a
    assert rp2 in a
    assert not (rp2 not in a)
    assert rp3 not in a
    assert not (rp3 in a)
