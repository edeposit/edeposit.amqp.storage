#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import base64

import pytest

import test_storage_handler
from test_storage_handler import data_context
from structures.test_db_publication import random_publication

import storage


# Variables ===================================================================
EBOOK_FN = "ebook.pdf"


# Fixtures ====================================================================
@pytest.fixture
def pdf_file():
    return data_context(EBOOK_FN, mode="rb")


@pytest.fixture
def b64_pdf_file():
    return base64.b64encode(pdf_file())


@pytest.fixture
def pdf_publication(tmpdir):
    tmp_file = tmpdir.join(EBOOK_FN)
    tmp_file.write_binary(pdf_file())

    pub = random_publication()
    pub.file_pointer = str(tmp_file)
    pub.filename = EBOOK_FN

    return pub.to_comm()


# Setup =======================================================================
def setup_module(module):
    test_storage_handler.setup_module(module)


def teardown_module(module):
    test_storage_handler.teardown_module(module)


# Tests =======================================================================
def test_publication(pdf_publication, b64_pdf_file):
    assert pdf_publication
    assert pdf_publication.filename == EBOOK_FN
    assert pdf_publication.b64_data == b64_pdf_file


def test_publication_save(pdf_publication):
    storage.reactToAMQPMessage(
        storage.SaveRequest(pdf_publication)
    )

    result = storage.reactToAMQPMessage(
        storage.SearchRequest(storage.Publication(pdf_publication.isbn))
    )

    assert result.publications
    assert result.publications[0] == pdf_publication
