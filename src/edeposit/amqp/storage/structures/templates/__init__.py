#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path
from bottle import template

import shared
from shared import SAVEABLE_FIELDS


# Functions ===================================================================
def _apply_template(my_template):
    return template(
        my_template,
        CLASS_NAME=shared.CLASS_NAME,
        COMMUNICATION_FIELDS=shared.COMMUNICATION_FIELDS,
        DATABASE_FIELDS=shared.DATABASE_FIELDS,
        SAVEABLE_FIELDS=shared.SAVEABLE_FIELDS,
    )


def _read_file(fn):
    fn = os.path.join(
        os.path.dirname(__file__),
        fn
    )

    with open(fn) as f:
        return f.read()


def get_db_publication():
    return _apply_template(
        _read_file("db_publication_template.py")
    )


def get_publication():
    return _apply_template(
        _read_file("publication_template.py")
    )
