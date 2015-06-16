#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import uuid
import random
import copy

from BTrees.OOBTree import OOTreeSet

import pytest
from faker import Factory

from storage.structures import DBPublication


# Variables ===================================================================
FAKER = Factory.create('cs_CZ')


# Fixtures ====================================================================
@pytest.fixture
def random_publication():
    return DBPublication(
        title=FAKER.text(20),
        author=FAKER.name(),
        pub_year="%04d" % random.randint(1990, 2015),
        isbn=FAKER.ssn(),
        urnnbn="urn:nbn:cz:edep002-00%04d" % random.randint(0, 999),
        uuid=str(uuid.uuid4()),
        is_public=True,
        filename="/home/xex.pdf",
        file_pointer="/tmp/uuid287378",
    )


# Tests =======================================================================
def test_op_eq(random_publication):
    rand_copy = copy.deepcopy(random_publication)

    assert random_publication == rand_copy
    # assert random_publication.__hash__() == rand_copy.__hash__()
    assert not (random_publication != rand_copy)

    rand_copy.title = "azgabash"

    assert not (random_publication == rand_copy)  # op eq
    # assert random_publication.__hash__() != rand_copy.__hash__()
    assert random_publication != rand_copy


def test_in_operator():
    rp1 = random_publication()
    rp2 = random_publication()
    rp3 = random_publication()

    assert rp1 != rp2

    cont = set([rp1, rp2])

    assert rp1 in cont
    assert rp2 in cont

    assert rp3 not in cont


def test_OOTreeSet():
    a = OOTreeSet()
    rp1 = random_publication()
    rp2 = random_publication()
    rp3 = random_publication()

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
