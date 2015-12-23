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
from functools import partial
from urllib import unquote_plus

from bottle import run
from bottle import abort
from bottle import error
from bottle import route
from bottle import HTTPError
from bottle import static_file
from bottle import SimpleTemplate

import mime
from bottle import auth_basic

sys.path.insert(0, join(dirname(__file__), "../src/edeposit/amqp"))

try:
    from storage import DBPublication
    from storage.tree_handler import tree_handler
    from storage.publication_storage import search_publications
    from storage.publication_storage import search_pubs_by_uuid

    from storage import settings
    from storage import web_tools
except ImportError:
    from edeposit.amqp.storage import DBPublication
    from edeposit.amqp.storage.tree_handler import tree_handler
    from edeposit.amqp.storage.publication_storage import search_publications
    from edeposit.amqp.storage.publication_storage import search_pubs_by_uuid

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
          <a href="{{compose_path(pub, uuid_url=True)}}">{{pub.title}}</a>
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


TREES_TEMPLATE = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="cs" xml:lang="cs">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Seznam publikací periodika</title>
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
        .link_up {
            float: right;
        }
        .sub_tree {
            margin-left: 1em;
        }
    </style>
</head>
<body>
% if link_up:
    <a class="link_up" href="{{link_up}}">[Zpět]</a>
% end

% for tree in trees:
<h1>Seznam publikací periodika <em>{{tree.name}}</em></h1>

    {{ !render_tree(tree, 1) }}

% end

</body>
</html>
"""


TREE_TEMPLATE = """
<div class="sub_tree">
  <h2><a href="{{path_composer(tree)}}">{{tree.name}}</a></h2>

% for sub_tree in tree.sub_trees:
    {{!render_tree(sub_tree, ind+1)}}
% end

% if tree.sub_publications:
  <ul>
%   for sub_publication_uuid in tree.sub_publications:
%     pub = pub_cache[sub_publication_uuid]

%     if pub.is_public:
    <li><a href="{{pub.url}}">{{ pub.title }}</a></li>
%     else:
    <li>{{ pub.title }} <em>(neveřejný zdroj)</em></li>
%     end
%   end
  </ul>

</div>
"""


# Functions & classes =========================================================
@error(403)
def error403(error):
    """
    Custom 403 page.
    """
    tb = error.traceback

    if isinstance(tb, dict) and "name" in tb and "uuid" in tb:
        return SimpleTemplate(PRIVATE_ACCESS_MSG).render(
            name=error.traceback["name"],
            uuid=error.traceback["uuid"]
        )

    return "Access denied!"


@route(join("/", settings.UUID_DOWNLOAD_KEY, "<uuid>"))
def fetch_by_uuid(uuid):
    """
    Serve publications by UUID.
    """
    # fetch all - private and public - publications
    all_pubs = [
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

    mime_type = mime.Types.of(down_fn)[0].content_type
    if mime_type == "inode/symlink":
        mime_type = "auto"

    response = static_file(
        local_fn,
        root=settings.PUBLIC_DIR,
        download=down_fn,
        mimetype=mime_type,
    )

    # Bottle doesn't allow you to specify custom filename AND to say, that you
    # want to have this file for view in browser instead of download. This
    # happens because it uses `download` parameter as both bool flag and
    # alternative filename. - this hack allows it.
    if mime_type == "application/pdf":
        disposition = 'inline; filename="%s"' % down_fn
        response.headers[str("Content-Disposition")] = str(disposition)

    return response


def render_trees(trees, path_composer):
    """
    Render list of `trees` to HTML.

    Args:
        trees (list): List of :class:`.Tree`.
        path_composer (fn reference): Function used to compose paths from UUID.
            Look at :func:`.compose_tree_path` from :mod:`.web_tools`.

    Returns:
        str: HTML representation of trees.
    """
    trees = list(trees)  # by default, this is set

    def create_pub_cache(trees):
        """
        Create uuid -> DBPublication cache from all uuid's linked from `trees`.

        Args:
            trees (list): List of :class:`.Tree`.

        Returns:
            dict: {uuid: DBPublication}
        """
        sub_pubs_uuids = sum((x.collect_publications() for x in trees), [])

        uuid_mapping = {
            uuid: search_pubs_by_uuid(uuid)
            for uuid in set(sub_pubs_uuids)
        }

        # cleaned dict without blank matches
        return {
            uuid: pub[0]
            for uuid, pub in uuid_mapping.iteritems()
            if pub
        }

    # create uuid -> DBPublication cache
    pub_cache = create_pub_cache(trees)

    def render_tree(tree, ind=1):
        """
        Render the tree into HTML using :attr:`TREE_TEMPLATE`. Private trees
        are ignored.

        Args:
            tree (obj): :class:`.Tree` instance.
            ind (int, default 1): Indentation. This function is called
                recursively.

        Returns:
            str: Rendered string.
        """
        if not tree.is_public:
            return ""

        rendered_tree = SimpleTemplate(TREE_TEMPLATE).render(
            tree=tree,
            render_tree=render_tree,
            ind=ind,
            path_composer=path_composer,
            pub_cache=pub_cache,
        )

        # keep nice indentation
        ind_txt = ind * "  "
        return ind_txt + ("\n" + ind_txt).join(rendered_tree.splitlines())

    # this is used to get reference for back button
    parent = tree_handler().get_parent(trees[0])
    link_up = path_composer(parent) if parent else None

    return SimpleTemplate(TREES_TEMPLATE).render(
        trees=trees,
        render_tree=render_tree,
        link_up=link_up,
    )


@route(join("/", settings.ISSN_DOWNLOAD_KEY, "<issn>"))
def show_periodical_tree_by_issn(issn):
    """
    Render tree using ISSN.
    """
    trees = tree_handler().trees_by_issn(issn)

    if not trees:
        abort(404, "Dokument s ISSN '%s' není dostupný." % issn)

    return render_trees(
        trees,
        partial(web_tools.compose_tree_path, issn=True)
    )


@route(join("/", settings.PATH_DOWNLOAD_KEY, "<path:path>"))
def show_periodical_tree_by_path(path):
    """
    Render tree using it's path.
    """
    path = unquote_plus(path)
    trees = tree_handler().trees_by_path(path)

    if not trees:
        path = path.decode("utf-8")
        abort(404, "Dokument s názvem '%s' není dostupný." % path)

    return render_trees(
        trees,
        partial(web_tools.compose_tree_path, issn=False)
    )


def list_publications():
    """
    Return list of all publications in basic graphic HTML render.
    """
    publications = search_publications(
        DBPublication(is_public=True)
    )

    return SimpleTemplate(INDEX_TEMPLATE).render(
        publications=publications,
        compose_path=web_tools.compose_path,
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
        debug=settings.WEB_DEBUG,
        reloader=settings.WEB_RELOADER,
    )
