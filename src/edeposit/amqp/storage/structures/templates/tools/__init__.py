#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

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
