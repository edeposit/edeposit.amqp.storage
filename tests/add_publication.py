#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
from os.path import join, dirname

sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))
from storage import storage_handler

from structures.test_db_publication import random_publication


# Variables ===================================================================
# Functions & classes =========================================================
def add_publication():
    pub = random_publication()
    storage_handler.save_publication(pub)

    return pub


# Main program ================================================================
if __name__ == '__main__':
    pub = add_publication()
    print "Added", pub.title
