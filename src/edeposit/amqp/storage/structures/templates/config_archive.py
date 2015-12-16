#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from tools import Field
from tools import read_file
from tools import apply_template


# Variables ===================================================================
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


# Functions ===================================================================
def get_db_archive():
    return apply_template(
        my_template=read_file("templates/db_template.pyt"),
        fields=FIELDS,
        class_name="Archive",
    )


def get_archive():
    return apply_template(
        my_template=read_file("templates/comm_template.pyt"),
        fields=FIELDS,
        class_name="Archive",
    )
