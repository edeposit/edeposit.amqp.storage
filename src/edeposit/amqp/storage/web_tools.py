#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urllib import quote_plus

from os.path import join
from os.path import basename

from settings import WEB_ADDR
from settings import WEB_PORT
from settings import DOWNLOAD_KEY
from settings import UUID_DOWNLOAD_KEY
from settings import ISSN_DOWNLOAD_KEY
from settings import PATH_DOWNLOAD_KEY


# Variables ===================================================================
_PROTOCOL = "http"


# Functions & classes =========================================================
class PrivatePublicationError(UserWarning):
    """
    Indication that publication is private.
    """


def compose_path(pub, uuid_url=False):
    """
    Compose absolute path for given `pub`.

    Args:
        pub (obj): :class:`.DBPublication` instance.
        uuid_url (bool, default False): Compose URL using UUID.

    Returns:
        str: Absolute url-path of the publication, without server's address \
             and protocol.

    Raises:
        PrivatePublicationError: When the `pub` is private publication.
    """
    if uuid_url:
        return join(
            "/",
            UUID_DOWNLOAD_KEY,
            basename(pub.uuid)
        )

    return join(
        "/",
        DOWNLOAD_KEY,
        basename(pub.file_pointer),
        basename(pub.filename)
    )


def compose_tree_path(tree, issn=False):
    """
    Compose absolute path for given `tree`.

    Args:
        pub (obj): :class:`.Tree` instance.
        issn (bool, default False): Compose URL using ISSN.

    Returns:
        str: Absolute path of the tree, without server's address and protocol.
    """
    if issn:
        return join(
            "/",
            ISSN_DOWNLOAD_KEY,
            basename(tree.issn)
        )

    return join(
        "/",
        PATH_DOWNLOAD_KEY,
        quote_plus(tree.path),
    )


def compose_full_url(pub, uuid_url=False):
    """
    Compose full url for given `pub`, with protocol, server's address and port.

    Args:
        pub (obj): :class:`.DBPublication` instance.
        uuid_url (bool, default False): Compose URL using UUID.

    Returns:
        str: Absolute url of the publication.
    Raises:
        PrivatePublicationError: When the `pub` is private publication.
    """
    url = compose_path(pub, uuid_url)

    if WEB_PORT == 80:
        return "%s://%s%s" % (_PROTOCOL, WEB_ADDR, url)

    return "%s://%s:%d%s" % (_PROTOCOL, WEB_ADDR, WEB_PORT, url)


def compose_tree_url(tree, issn_url=False):
    """
    Compose full url for given `tree`, with protocol, server's address and
    port.

    Args:
        tree (obj): :class:`.Tree` instance.
        issn_url (bool, default False): Compose URL using ISSN.

    Returns:
        str: URL of the tree
    """
    url = compose_tree_path(tree, issn_url)

    if WEB_PORT == 80:
        return "%s://%s%s" % (_PROTOCOL, WEB_ADDR, url)

    return "%s://%s:%d%s" % (_PROTOCOL, WEB_ADDR, WEB_PORT, url)
