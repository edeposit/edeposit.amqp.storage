#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import structures

from structures import Publication
from structures import DBPublication as _DBPublication

from structures import SaveRequest
from structures import SearchResult
from structures import SearchRequest

from storage_handler import save_publication
from storage_handler import search_publications


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
        return save_publication(
            _DBPublication.from_comm(message.pub)
        )

    elif _instanceof(message, SearchRequest):
        results = search_publications(
            _DBPublication.from_comm(message.query)
        )

        return SearchResult(
            publications=[_DBPublication.to_comm(pub) for pub in results]
        )

    raise ValueError("'%s' is unknown type of request!" % str(type(message)))
