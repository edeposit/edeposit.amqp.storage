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
        name="title",
        docstring="(str): Title of the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="author",
        docstring="(str): Name of the author.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="pub_year",
        docstring="(str): Year when the publication was released.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="isbn",
        docstring="(str): ISBN for the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="urnnbn",
        docstring="(str): URN:NBN for the publication.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="uuid",
        docstring="(str): UUID string to pair the publication with edeposit.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="aleph_id",
        docstring="(str): ID used in aleph.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="producent_id",
        docstring="(str): ID used for producent.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="is_public",
        docstring="(bool): Is the file public?",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="filename",
        docstring="(str): Original filename.",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="is_periodical",
        docstring="(bool): Is the publication periodical?",
        is_comm_field=True,
        is_db_field=True,
    ),
    Field(
        name="path",
        docstring="(str): Path in the tree (used for periodicals).",
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
    Field(
        name="url",
        docstring="(str): URL in case that publication is public.",
        is_comm_field=True,
        is_db_field=False,
        is_saveable=False,
    ),

    # DB fields
    Field(
        name="file_pointer",
        docstring="(str): Pointer to the file on the file server.",
        is_comm_field=True,
        is_db_field=True,
        is_saveable=False,
    ),
]


# Functions ===================================================================
def get_db_publication():
    return apply_template(
        read_file("templates/db_template.pyt"),
        fields=FIELDS,
        class_name="Publication",
    )


def get_publication():
    return apply_template(
        read_file("templates/comm_template.pyt"),
        fields=FIELDS,
        class_name="Publication",
    )
