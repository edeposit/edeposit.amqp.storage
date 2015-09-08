#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path
from bottle import template

import publication_config


# Functions ===================================================================
def _apply_publication_template(my_template):
    return template(
        my_template,
        CLASS_NAME=publication_config.CLASS_NAME,
        COMMUNICATION_FIELDS=publication_config.COMMUNICATION_FIELDS,
        DATABASE_FIELDS=publication_config.DATABASE_FIELDS,
        SAVEABLE_FIELDS=publication_config.SAVEABLE_FIELDS,
    )


def _read_file(fn):
    fn = os.path.join(
        os.path.dirname(__file__),
        fn
    )

    with open(fn) as f:
        return f.read()


def get_db_publication():
    return _apply_publication_template(
        _read_file("db_template.pyt")
    )


def get_publication():
    return _apply_publication_template(
        _read_file("comm_template.pyt")
    )
