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

from bottle import run
from bottle import abort
from bottle import error
from bottle import route
from bottle import HTTPError
from bottle import static_file
from bottle import SimpleTemplate

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
% for pub in publications:
  <div class="publication">
    <table>
      <tr>
        <td colspan='4' class="title_link">
          <a href="{{compose_url(pub, uuid_url=True)}}">{{pub.title}}</a>
        </td>
      </tr>
      <tr>
        <td class="author">Autor{{delimiter}}</td>
        <td class="author_content">{{pub.author}}</td>

        <td class="isbn">ISBN{{delimiter}}</td>
        <td class="isbn_content">{{pub.isbn}}</td>
      </tr>
      <tr>
        <td class="year">Rok vydání{{delimiter}}</td>
        <td class="year_content">{{pub.pub_year}}</td>

        <td class="urn_nbn">URN:NBN{{delimiter}}</td>
        <td class="urn_nbn_content">{{pub.urnnbn}}</td>
      </tr>
    </table>
  </div>
% end
</div>

</body>
</html>
"""


PRIVATE_ACCESS_MSG = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
    <title>Veřejně nepřístupný dokument</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
      html {background-color: #eee; font-family: sans;}
      body {background-color: #fff; border: 1px solid #ddd;
            padding: 15px; margin: 15px;}
      div {background-color: #eee; border: 1px solid #ddd; padding-left: 10px;}
    </style>
</head>
<body>
    <h1>Chyba: Veřejně nepřístupný dokument</h1>
    <div>
    <p>
      Dokument <em>`{{name}}`</em> s UUID <tt>`{{uuid}}`</tt> bohužel není
      veřejně přístupný.
    </p>

    <p>
      Tato publikace je zpřístupněna pouze na terminálech v prostorech
      <a href="http://www.nkp.cz/">Národní knihovny ČR</a>.
    </p>
    </div>
</body>
</html>
"""


# Functions & classes =========================================================
@error(403)
def error403(error):
    tb = error.traceback

    if isinstance(tb, dict) and "name" in tb and "uuid" in tb:
        return SimpleTemplate(PRIVATE_ACCESS_MSG).render(
            name=error.traceback["name"],
            uuid=error.traceback["uuid"]
        )

    return "Access denied!"


@zconf.cached_connection(timeout=settings.WEB_DB_TIMEOUT)
def search_publications_closure(*args, **kwargs):
    """
    Use cached connection.
    """
    return search_publications(*args, **kwargs)


@route(join("/", settings.UUID_DOWNLOAD_KEY, "<uuid>"))
def fetch_by_uuid(uuid):
    """
    Serve publications by UUID.
    """
    # fetch all - private and public - publications
    all_pubs = [
        pub
        for pub in search_publications_closure(DBPublication(uuid=uuid))
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
        raise HTTPError(
            403,
            body="Forbidden!",
            traceback={"name": name.decode("utf-8"), "uuid": uuid}
        )

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

    return SimpleTemplate(INDEX_TEMPLATE).render(
        publications=publications,
        compose_url=web_tools.compose_url,
        delimiter=":",
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
