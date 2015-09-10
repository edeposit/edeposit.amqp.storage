#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import base64
import os.path
import tempfile

import pytest

import environment_generator
from environment_generator import data_context
from structures.test_db_archive import random_archive_comm
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

    assert result.records

    assert result.records[0].title == pdf_publication.title
    assert result.records[0].author == pdf_publication.author
    assert result.records[0].pub_year == pdf_publication.pub_year
    assert result.records[0].isbn == pdf_publication.isbn
    assert result.records[0].urnnbn == pdf_publication.urnnbn
    assert result.records[0].uuid == pdf_publication.uuid
    assert result.records[0].aleph_id == pdf_publication.aleph_id
    assert result.records[0].producent_id == pdf_publication.producent_id
    assert result.records[0].is_public == pdf_publication.is_public
    assert result.records[0].filename == pdf_publication.filename
    assert len(result.records[0].b64_data) > 100
    assert "http" in result.records[0].url


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

    assert result.records

    assert result.records[0].title == pdf_publication.title
    assert result.records[0].author == pdf_publication.author
    assert result.records[0].pub_year == pdf_publication.pub_year
    assert result.records[0].isbn == pdf_publication.isbn
    assert result.records[0].urnnbn == pdf_publication.urnnbn
    assert result.records[0].uuid == pdf_publication.uuid
    assert result.records[0].aleph_id == pdf_publication.aleph_id
    assert result.records[0].producent_id == pdf_publication.producent_id
    assert result.records[0].is_public == pdf_publication.is_public
    assert result.records[0].filename == pdf_publication.filename
    assert not result.records[0].b64_data
    assert "http" in result.records[0].url


def test_archive_save(random_archive_comm):
    path = storage.reactToAMQPMessage(
        storage.SaveRequest(random_archive_comm),
        lambda x: x
    ).dir_pointer

    assert os.path.exists(path)
    assert os.path.isdir(path)

    assert os.path.exists(os.path.join(path, "ebook.pdf"))
    assert os.path.exists(os.path.join(path, "zeo.conf"))
    assert os.path.exists(os.path.join(path, "zeo_client.conf"))

    assert os.path.isfile(os.path.join(path, "ebook.pdf"))
    assert os.path.isfile(os.path.join(path, "zeo.conf"))
    assert os.path.isfile(os.path.join(path, "zeo_client.conf"))

    result = storage.reactToAMQPMessage(
        storage.SearchRequest(
            storage.Archive(isbn=random_archive_comm.isbn)
        ),
        lambda x: x
    )

    assert result.records

    assert result.records[0].isbn == random_archive_comm.isbn
    assert result.records[0].uuid == random_archive_comm.uuid
    assert result.records[0].aleph_id == random_archive_comm.aleph_id

    assert len(result.records[0].b64_data) > 100


def test_archive_light_request(random_archive_comm):
    storage.reactToAMQPMessage(
        storage.SaveRequest(random_archive_comm),
        lambda x: x
    )

    result = storage.reactToAMQPMessage(
        storage.SearchRequest(
            storage.Archive(isbn=random_archive_comm.isbn),
            light_request=True
        ),
        lambda x: x
    )

    assert result.records

    assert result.records[0].isbn == random_archive_comm.isbn
    assert result.records[0].uuid == random_archive_comm.uuid
    assert result.records[0].aleph_id == random_archive_comm.aleph_id

    assert not result.records[0].b64_data
