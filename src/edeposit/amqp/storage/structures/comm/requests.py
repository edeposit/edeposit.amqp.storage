#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from archive import Archive
from publication import Publication
from tree import Tree


# Functions & classes =========================================================
class SearchRequest(namedtuple("SearchRequest", ["query", "light_request"])):
    """
    Retreive publication from archive using `query` - instance of
    :class:`.Publication` or :class:`.Archive`. Any property of the is used to
    retreive data.

    Attributes:
        query (obj): Instance of :class:`.Publication` or :class:`.Archive`.
        light_request (bool, default False): If true, don't return the data.
                      This is used when you need just the metadata info.
    """
    def __new__(self, query, light_request=False):
        return super(SearchRequest, self).__new__(self, query, light_request)

    def __init__(self, query, light_request=False):
        SearchRequest._check_record_type(query)

        super(self.__class__, self).__init__(query, light_request)

    @staticmethod
    def _check_record_type(q):
        def check_type(q):
            return (
                isinstance(q, Publication) or
                isinstance(q, Archive) or
                isinstance(q, Tree)
            )

        assert check_type(q), "Publication instance is expected!"


class SaveRequest(namedtuple("SaveRequest", ["record"])):
    """
    Save `record` to the storage.

    Attributes:
        record (obj): Instance of the :class:`.Publication`,
        :class:`.Archive`.
    """
    def __init__(self, record):
        SearchRequest._check_record_type(record)

        super(self.__class__, self).__init__(record)
