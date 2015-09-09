#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from archive import Archive
from publication import Publication


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

        self.query = query
        self.__dict__["light_request"] = light_request

    @staticmethod
    def _check_record_type(q):
        msg = "Publication instance is expected!"
        assert isinstance(q, Publication) or isinstance(q, Archive), msg

    @property
    def query(self):
        return self.__dict__["query"]

    @query.setter
    def query(self, q):
        SearchRequest._check_record_type(q)

        self.__dict__["query"] = q


class SaveRequest(namedtuple("SaveRequest", ["record"])):
    """
    Save `record` to the storage.

    Attributes:
        record (obj): Instance of the :class:`.Publication` or
        :class:`.Archive`.
    """
    def __init__(self, record):
        SearchRequest._check_record_type(record)

        self.record = record

    @property
    def record(self):
        return self.__dict__["record"]

    @record.setter
    def record(self, q):
        SearchRequest._check_record_type(q)

        self.__dict__["record"] = q
