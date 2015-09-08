#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from bottle import template

from field import Field
from shared import read_file


# Variables ===================================================================
CLASS_NAME = "Archive"

FIELDS = [
    Field(
        name="isbn",
        docstring="(str): ISBN for the archive.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="uuid",
        docstring="(str): UUID string to pair the archive with edeposit.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="aleph_id",
        docstring="(str): ID used in aleph.",
        is_comm_field=True,
        is_db_field=True,
    ),

    # comm fields
    Field(
        name="b64_data",
        docstring="(str): Base64 encoded data ebook file.",
        is_comm_field=True,
        is_db_field=False,
        is_saveable=False,
    ),

    # DB fields
    Field(
        name="dir_pointer",
        docstring="(str): Pointer to the directory on the file server.",
        is_comm_field=True,
        is_db_field=True,
        is_saveable=False,
    ),
]

COMMUNICATION_FIELDS = [
    field
    for field in FIELDS
    if field.is_comm_field
]

SAVEABLE_FIELDS = [
    field
    for field in FIELDS
    if field.is_saveable
]

DATABASE_FIELDS = [
    field
    for field in FIELDS
    if field.is_db_field
]


def _apply_archive_template(my_template):
    return template(
        my_template,
        CLASS_NAME=CLASS_NAME,
        COMMUNICATION_FIELDS=COMMUNICATION_FIELDS,
        DATABASE_FIELDS=DATABASE_FIELDS,
        SAVEABLE_FIELDS=SAVEABLE_FIELDS,
    )


def get_db_archive():
    return _apply_archive_template(
        read_file("db_template.pyt")
    )


def get_archive():
    return _apply_archive_template(
        read_file("comm_template.pyt")
    )
