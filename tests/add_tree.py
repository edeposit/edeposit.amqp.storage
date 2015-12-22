#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import uuid
import base64
import random
from os.path import join, dirname

from faker import Factory


sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))

import storage
from storage import Publication
from structures.test_tree import sample_tree



# Variables ===================================================================
FAKER = Factory.create('cs_CZ')


# Functions & classes =========================================================
def _pdf_file():
    fn = join(dirname(__file__), "data/ebook.pdf")

    with open(fn) as f:
        return f.read()


def _b64_pdf_file():
    return base64.b64encode(
        _pdf_file()
    )


def _publication(public=True):
    return Publication(
        title=FAKER.text(20),
        author=FAKER.name(),
        pub_year="%04d" % random.randint(1990, 2015),
        isbn=FAKER.ssn(),
        urnnbn="urn:nbn:cz:edep002-00%04d" % random.randint(0, 999),
        uuid=str(uuid.uuid4()),
        is_public=public,
        is_periodical=True,
        b64_data=_b64_pdf_file(),
        filename="/home/xex.pdf",
    )


def add_publication():
    pub = _publication(True)

    print "storing", pub.uuid

    pub = storage.reactToAMQPMessage(
        storage.SaveRequest(pub),
        lambda x: x
    )

    return pub


def add_tree():
    tree = sample_tree()

    tree.sub_trees[0].sub_publications.pop()
    tree.sub_trees[0].sub_publications.pop()

    tree.sub_trees[1].sub_publications.pop()
    tree.sub_trees[1].sub_publications.pop()

    tree.sub_publications.append(add_publication().uuid)
    tree.sub_publications.append(add_publication().uuid)

    tree.sub_trees[0].sub_publications.append(add_publication().uuid)
    tree.sub_trees[0].sub_publications.append(add_publication().uuid)

    tree.sub_trees[1].sub_publications.append(add_publication().uuid)
    tree.sub_trees[1].sub_publications.append(add_publication().uuid)

    return storage.reactToAMQPMessage(
        storage.SaveRequest(tree),
        lambda x: x
    )


# Main program ================================================================
if __name__ == '__main__':
    pub = add_tree()

    print "Added\t", pub
    print
    print pub
