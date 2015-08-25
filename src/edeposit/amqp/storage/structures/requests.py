#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from publication import Publication


# Functions & classes =========================================================
class SearchRequest(namedtuple("SearchRequest", ["query", "light_request"])):
    """
    Retreive publication from archive using `query` - instance of
    :class:`.Publication`. Any property of the is used to retreive data.

    Attributes:
        query (obj): Instance of the :class:`.Publication`.
        light_request (bool, default False): If true, don't return the data.
                      This is used when you need just the metadata info.
    """
    def __new__(self, query, light_request=False):
        return super(SearchRequest, self).__new__(self, query, light_request)

    def __init__(self, query, light_request=False):
        SearchRequest._check_pub_type(query)

        self.query = query
        self.__dict__["light_request"] = light_request

    @staticmethod
    def _check_pub_type(q):
        assert isinstance(q, Publication), "Publication instance is expected!"

    @property
    def query(self):
        return self.__dict__["query"]

    @query.setter
    def query(self, q):
        SearchRequest._check_pub_type(q)

        self.__dict__["query"] = q


class SaveRequest(namedtuple("SaveRequest", ["pub"])):
    """
    Save :class:`.Publication` to the storage.

    Attributes:
        pub (obj): Instance of the :class:`.Publication`.
    """
    def __init__(self, pub):
        SearchRequest._check_pub_type(pub)

        self.pub = pub

    @property
    def pub(self):
        return self.__dict__["pub"]

    @pub.setter
    def pub(self, q):
        SearchRequest._check_pub_type(q)

        self.__dict__["pub"] = q
