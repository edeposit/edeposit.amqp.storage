#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# !!! DO NOT EDIT THIS FILE - THIS IS GENERATED FILE !!!
# Imports =====================================================================
from functools import total_ordering

from kwargs_obj import KwargsObj
from persistent import Persistent

from storage.settings import TREE_PROJECT_KEY as PROJECT_KEY

from storage.structures.comm.tree import Tree


# Functions and classes =======================================================
@total_ordering
class DBTree(Persistent, KwargsObj):
    '''
    Database structure used to store basic metadata about Trees.
    '''
    def __init__(self, **kwargs):
        for key in Tree._PUB_FIELDS:
            setattr(self, key, None)

        # transport the attribute help from the Tree
        self.__class__.__doc__ += "\n\n" + Tree.__doc__.split("\n\n", 1)[-1]

        self._kwargs_to_attributes(kwargs)

    @classmethod
    def from_comm(cls, pub):
        '''
        Convert communication namedtuple to this class.

        Args:
            pub (obj): :class:`.Tree` instance which will be converted.

        Returns:
            obj: :class:`DBTree` instance.
        '''
        return cls(**pub._as_dict())

    @property
    def indexes(self):
        """
        Returns:
            list: List of strings, which may be used as indexes in DB.
        """
        return self.__dict__.keys()

    def to_comm(self, light_request=False):
        '''
        Convert `self` to :class:`.Tree`.

        Returns:
            obj: :class:`.Tree` instance.
        '''

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        for item_name in Tree._PUB_FIELDS:
            if not hasattr(self, item_name) or not hasattr(self, obj):
                return False

            if getattr(self, item_name) != getattr(self, obj):
                return False

        return True

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __lt__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        return self.path.__lt__(obj.path)
