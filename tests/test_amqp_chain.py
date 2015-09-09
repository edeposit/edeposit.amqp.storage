#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import base64
import tempfile

import pytest

import environment_generator
from environment_generator import data_context
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
def pdf_publication(random_publication):
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(pdf_file())
        tmp_file.seek(0)

        pub = random_publication
        pub.file_pointer = tmp_file.name
        pub.filename = EBOOK_FN

        return pub.to_comm()


# Setup =======================================================================
def setup_module(module):
    environment_generator.generate_environment()


def teardown_module(module):
    environment_generator.cleanup_environment()


# Tests =======================================================================
def test_publication(pdf_publication, b64_pdf_file):
    assert pdf_publication
    assert pdf_publication.filename == EBOOK_FN

    # remove all whitespaces
    pub_data = "".join(pdf_publication.b64_data.split())
    b64_pdf_file_data = "".join(b64_pdf_file.split())

    assert pub_data == b64_pdf_file_data


def test_publication_save(pdf_publication):
    storage.reactToAMQPMessage(
        storage.SaveRequest(pdf_publication),
        lambda x: x
    )

    result = storage.reactToAMQPMessage(
        storage.SearchRequest(
            storage.Publication(isbn=pdf_publication.isbn)
        ),
        lambda x: x
    )

    assert result.publications

    assert result.publications[0].title == pdf_publication.title
    assert result.publications[0].author == pdf_publication.author
    assert result.publications[0].pub_year == pdf_publication.pub_year
    assert result.publications[0].isbn == pdf_publication.isbn
    assert result.publications[0].urnnbn == pdf_publication.urnnbn
    assert result.publications[0].uuid == pdf_publication.uuid
    assert result.publications[0].aleph_id == pdf_publication.aleph_id
    assert result.publications[0].producent_id == pdf_publication.producent_id
    assert result.publications[0].is_public == pdf_publication.is_public
    assert result.publications[0].filename == pdf_publication.filename
    assert len(result.publications[0].b64_data) > 100
    assert "http" in result.publications[0].url


def test_publication_light_request(pdf_publication):
    storage.reactToAMQPMessage(
        storage.SaveRequest(pdf_publication),
        lambda x: x
    )

    result = storage.reactToAMQPMessage(
        storage.SearchRequest(
            storage.Publication(isbn=pdf_publication.isbn),
            light_request=True
        ),
        lambda x: x
    )

    assert result.publications

    assert result.publications[0].title == pdf_publication.title
    assert result.publications[0].author == pdf_publication.author
    assert result.publications[0].pub_year == pdf_publication.pub_year
    assert result.publications[0].isbn == pdf_publication.isbn
    assert result.publications[0].urnnbn == pdf_publication.urnnbn
    assert result.publications[0].uuid == pdf_publication.uuid
    assert result.publications[0].aleph_id == pdf_publication.aleph_id
    assert result.publications[0].producent_id == pdf_publication.producent_id
    assert result.publications[0].is_public == pdf_publication.is_public
    assert result.publications[0].filename == pdf_publication.filename
    assert not result.publications[0].b64_data
    assert "http" in result.publications[0].url
