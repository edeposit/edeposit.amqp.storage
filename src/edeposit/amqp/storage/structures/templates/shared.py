#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path


# Functions & classes =========================================================
def read_file(fn):
    fn = os.path.join(
        os.path.dirname(__file__),
        fn
    )

    with open(fn) as f:
        return f.read()
