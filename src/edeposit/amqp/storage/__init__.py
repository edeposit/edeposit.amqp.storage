#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import structures

from structures import Publication
from structures import DBPublication

from structures import Archive
from structures import DBArchive

from structures import SaveRequest
from structures import SearchResult
from structures import SearchRequest

from publication_storage import save_publication
from publication_storage import search_publications

from archive_storage import save_archive
from archive_storage import search_archives


# Functions & classes =========================================================
def _instanceof(instance, cls):
    """
    Check type of `instance` by matching ``.__name__`` with `cls.__name__`.
    """
    return type(instance).__name__ == cls.__name__


# Main function ===============================================================
def reactToAMQPMessage(message, send_back):
    """
    React to given (AMQP) message. `message` is expected to be
    :py:func:`collections.namedtuple` structure from :mod:`.structures` filled
    with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`.structures`.
        send_back (fn reference): Reference to function for responding. This is
                  useful for progress monitoring for example. Function takes
                  one parameter, which may be response structure/namedtuple, or
                  string or whatever would be normally returned.

    Returns:
        object: Response class from :mod:`structures`.

    Raises:
        ValueError: if bad type of `message` structure is given.
    """
    if _instanceof(message, SaveRequest):
        save_fn = save_publication
        class_ref = DBPublication

        if _instanceof(message.record, Archive):
            save_fn = save_archive
            class_ref = DBArchive

        return save_fn(
            class_ref.from_comm(message.record)
        )

    elif _instanceof(message, SearchRequest):
        search_fn = search_publications
        class_ref = DBPublication

        if _instanceof(message.query, Archive):
            search_fn = search_archives
            class_ref = DBArchive

        results = search_fn(
            class_ref.from_comm(message.query)
        )

        return SearchResult(
            records=[
                record.to_comm(light_request=message.light_request)
                for record in results
            ]
        )

    raise ValueError("'%s' is unknown type of request!" % str(type(message)))
