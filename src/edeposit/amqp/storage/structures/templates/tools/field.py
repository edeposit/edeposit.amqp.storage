#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class Field(object):
    def __init__(self, name, docstring, is_comm_field, is_db_field,
                 is_saveable=True):
        self.name = name
        self.docstring = docstring
        self.is_comm_field = is_comm_field
        self.is_db_field = is_db_field
        self.is_saveable = is_saveable

    def __repr__(self):
        return "Field(name)" % self.name
