#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

from bottle import template

from field import Field  # Just to make it available at package level


# Functions & classes =========================================================
def read_file(fn):
    fn = os.path.join(
        os.path.dirname(__file__),
        "../",
        fn
    )

    with open(fn) as f:
        return f.read()


def apply_template(my_template, fields, class_name):
    communication_fields = [
        field
        for field in fields
        if field.is_comm_field
    ]

    saveable_fields = [
        field
        for field in fields
        if field.is_saveable
    ]

    database_fields = [
        field
        for field in fields
        if field.is_db_field
    ]

    return template(
        my_template,
        CLASS_NAME=class_name,
        COMMUNICATION_FIELDS=communication_fields,
        DATABASE_FIELDS=database_fields,
        SAVEABLE_FIELDS=saveable_fields,
    )
