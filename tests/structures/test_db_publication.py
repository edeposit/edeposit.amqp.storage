#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import uuid
import random

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
# def test_():
#     pass
