#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from os.path import join
from os.path import basename

from settings import WEB_ADDR
from settings import WEB_PORT
from settings import DOWNLOAD_KEY


# Variables ===================================================================
_PROTOCOL = "http"


# Functions & classes =========================================================
class PrivatePublicationError(UserWarning):
    """
    Indication that publication is private.
    """


def compose_url(pub):
    """
    Compose absolute url for given `pub`.

    Args:
        pub (obj): :class:`.DBPublication` instance.

    Returns:
        str: Absolute url-path of the publication, without server's address \
             and protocol.

    Raises:
        PrivatePublicationError: When the `pub` is private publication.
    """
    if not pub.is_public:
        raise PrivatePublicationError("Publication is private!")

    return join(
        "/",
        DOWNLOAD_KEY,
        basename(pub.file_pointer),
        basename(pub.filename)
    )


def compose_full_url(pub):
    """
    Compose full url for given `pub`, with protocol, server's address and port.

    Args:
        pub (obj): :class:`.DBPublication` instance.

    Returns:
        str: Absolute url-path of the publication, without server's address \
             and protocol.

    Raises:
        PrivatePublicationError: When the `pub` is private publication.
    """
    if WEB_PORT == 80:
        return "%s://%s%s" % (_PROTOCOL, WEB_ADDR, compose_url(pub))

    return "%s://%s:%d%s" % (_PROTOCOL, WEB_ADDR, WEB_PORT, compose_url(pub))
