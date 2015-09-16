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

try:
    from storage import DBPublication
    from storage.publication_storage import search_publications

    from storage import zconf
    from storage import settings
    from storage import web_tools
except ImportError:
    from edeposit.amqp.storage import DBPublication
    from edeposit.amqp.storage.publication_storage import search_publications

    from edeposit.amqp.storage import zconf
    from edeposit.amqp.storage import settings
    from edeposit.amqp.storage import web_tools


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


PRIVATE_ACCESS_MSG = """Dokument `%s` s UUID `%s` bohužel není veřejně přístupný.

Obraťte se prosím na Národní knihovnu pro fyzické zpřístupnění na čtecím \
terminálu.
"""


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
        url=web_tools.compose_url(pub, uuid_url=True),
        delimiter=":"
    )


# @route(join("/", settings.DOWNLOAD_KEY, "<local_fn>", "<down_fn>"))
# def serve_static(local_fn, down_fn):
#     """
#     Serve static files. Make sure that user can't access other files on disk.
#     """
#     # remove slashes, leave only filename
#     down_fn = os.path.basename(down_fn)
#     local_fn = os.path.basename(local_fn)

#     full_path = join(settings.PUBLIC_DIR, local_fn)

#     if not os.path.exists(full_path):
#         abort(404, "'%s' není dostupný ke stažení." % local_fn)

#     return static_file(
#         local_fn,
#         root=settings.PUBLIC_DIR,
#         download=down_fn
#     )


@route(join("/", settings.UUID_DOWNLOAD_KEY, "<uuid>"))
def fetch_by_uuid(uuid):
    """
    Serve publication by UUID.
    """
    # fetch all - private and public - publications
    all_pubs =  [
        pub
        for pub in search_publications(DBPublication(uuid=uuid))
    ]

    if not all_pubs:
        abort(404, "Dokument s UUID '%s' není dostupný." % (uuid))

    public_pubs = [
        pub
        for pub in all_pubs
        if pub.is_public
    ]

    if not public_pubs:
        name = all_pubs[0].title
        abort(403, PRIVATE_ACCESS_MSG % (name, uuid))

    if len(public_pubs) > 1:
        abort(500, "Inkonzistence databáze - vráceno vícero UUID.")

    pub = public_pubs[0]

    if settings.PUBLIC_DIR not in pub.file_pointer:
        abort(500, "Pokus o neoprávněný přístup!")
    
    down_fn = os.path.basename(pub.filename)
    local_fn = pub.file_pointer.replace(settings.PUBLIC_DIR, "")

    return static_file(
        local_fn,
        root=settings.PUBLIC_DIR,
        download=down_fn
    )


@zconf.cached_connection(timeout=settings.WEB_DB_TIMEOUT)
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
        debug=False,
        reloader=True
    )
