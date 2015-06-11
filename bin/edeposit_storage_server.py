#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import os.path
from os.path import join
from os.path import dirname

from bottle import run
from bottle import abort
from bottle import route
from bottle import static_file

sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))

from storage.storage_handler import DBPublication
from storage.storage_handler import search_publications

from storage import settings


# Variables ===================================================================



# Functions & classes =========================================================
@route("/download/<book_fn>")
def serve_static(book_fn):
    book_fn = os.path.basename(book_fn)  # remove slashes, leave only filename
    full_path = join(settings.PUBLIC_DIR, book_fn)

    if not os.path.exists(full_path):
        abort(404, "%s is not available for download." % book_fn)

    return static_file(
        book_fn,
        root=settings.PUBLIC_DIR,
        download=True
    )


@route("/")
def index():
    publications = search_publications(
        DBPublication(is_public=True)
    )
    return "Here will be index"


# Main program ================================================================
if __name__ == '__main__':
    run(
        # server="paste",
        # host="",
        port=8080,
        debug=True,
        reloader=True
    )
