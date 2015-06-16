#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from __future__ import unicode_literals

import sys
import os.path
from os.path import join
from os.path import dirname
from string import Template

from bottle import run
from bottle import abort
from bottle import route
from bottle import static_file

from bottle import auth_basic

sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))

from storage.storage_handler import DBPublication
from storage.storage_handler import search_publications

from storage import settings


# Variables ===================================================================
INDEX_TEMPLATE = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="cs" xml:lang="cs">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Seznam veřejně přístupných publikací</title>
    <style>
        html {
            height: 95%;
        }
        body {
            display: block;
            margin: 0 auto;

            margin-top: 1em;
            margin-bottom: 1em;

            width: 56.2em;
            padding: 1em;

            border: 1px solid gray;
            text-align: justify;

            min-height: 95%;
        }
        h1 {
            text-align: center;
        }
        #content {
            margin-top: 5em;
        }
        .publication {
            border-top: 1px solid gray;
        }
        .title_link {
            font-size: 2em;
        }
        .author {
            width: 7em;
            font-weight: bold;
        }
        .isbn {
            width: 7em;
            font-weight: bold;
        }
        .urn_nbn {
            font-weight: bold;
        }
        .year {
            font-weight: bold;
        }
        .author_content, .year_content {
            width: 15em;
        }
    </style>
</head>
<body>
<h1>Seznam veřejně přístupných publikací projektu E-deposit</h1>

<div id="content">
$publications
</div>

</body>
</html>
"""

PUB_TEMPLATE = """<div class="publication">
<table>
    <tr>
        <td colspan='4' class="title_link"><a href="$url">$title</a></td>
    </tr>
    <tr>
        <td class="author">Autor$delimiter</td>
        <td class="author_content">$author</td>

        <td class="isbn">ISBN$delimiter</td>
        <td class="isbn_content">$isbn</td>
    </tr>
    <tr>
        <td class="year">Rok vydání$delimiter</td>
        <td class="year_content">$year</td>

        <td class="urn_nbn">URN:NBN$delimiter</td>
        <td class="urn_nbn_content">$urn_nbn</td>
    </tr>
</table>
</div>"""

DOWNLOAD_KEY = "download"  #: Used as part of the url


# Functions & classes =========================================================
def render_publication(pub):
    """
    Render `pub` (:class:`.DBPublication` instance) to HTML using
    :attr:`PUB_TEMPLATE`.
    """
    return Template(PUB_TEMPLATE).substitute(
        title=pub.title,
        author=pub.author,
        year=pub.pub_year,
        isbn=pub.isbn,
        urn_nbn=pub.urnnbn,
        url=join("/", DOWNLOAD_KEY, pub.uuid),
        delimiter=":"
    )


@route(join("/", DOWNLOAD_KEY, "<book_fn>"))
def serve_static(book_fn):
    """
    Serve static files. Make sure that user can't access other files on disk.
    """
    book_fn = os.path.basename(book_fn)  # remove slashes, leave only filename
    full_path = join(settings.PUBLIC_DIR, book_fn)

    if not os.path.exists(full_path):
        abort(404, "'%s' není dostupný ke stažení." % book_fn)

    return static_file(
        book_fn,
        root=settings.PUBLIC_DIR,
        download=True
    )


def list_publications():
    """
    Return list of all publications in basic graphic HTML render.
    """
    publications = search_publications(
        DBPublication(is_public=True)
    )

    publications = "\n".join(
        render_publication(pub)
        for pub in publications
    )

    return Template(INDEX_TEMPLATE).substitute(
        publications=publications
    )


def check_auth(username, password):
    """
    This function is used to check `username` and `password` in case that
    :attr:`.settings.PRIVATE_INDEX` is set to ``True`` (default is ``False``).
    """
    return (username == settings.PRIVATE_INDEX_USERNAME and
            settings.PRIVATE_INDEX_PASSWORD and
            password == settings.PRIVATE_INDEX_PASSWORD)


@auth_basic(check_auth)
def private_index():
    """
    Private index in case that login is enabled.
    """
    return list_publications()


@route("/")
def index():
    """
    Handle index of the project.
    """
    if not settings.PRIVATE_INDEX:
        return list_publications()

    return private_index()


# Main program ================================================================
if __name__ == '__main__':
    run(
        server=settings.WEB_SERVER,
        host=settings.WEB_ADDR,
        port=settings.WEB_PORT,
        debug=True,
        reloader=True
    )
