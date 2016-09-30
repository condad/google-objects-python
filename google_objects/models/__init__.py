# -*- coding: utf-8 -*-

from .drive import File, Permission
from .sheets import Spreadsheet, Sheet, Block
from .slides import Presentation, Page, Shape, Table

class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resources.
    """

    def __init__(self, **kwargs):
        # initalize  properties
        for key in kwargs.keys():
            self.__dict__['__{}'.format(key)] = kwargs.get(key)
