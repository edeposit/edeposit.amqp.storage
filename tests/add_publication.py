#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
from os.path import join, dirname

sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))
import storage

import test_amqp_chain


# Variables ===================================================================
# Functions & classes =========================================================
def add_publication():
    pub = test_amqp_chain.pdf_publication()
    storage.reactToAMQPMessage(
        storage.SaveRequest(pub),
        lambda x: x
    )

    return pub


# Main program ================================================================
if __name__ == '__main__':
    pub = add_publication()
    print "Added", pub.title
