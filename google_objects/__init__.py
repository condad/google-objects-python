# -*- coding: utf-8 -*-

# for ease of importing
from clients import DriveAPI, SheetsAPI


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resources.
    """

    def __init__(self, **kwargs):
        # initalize  properties
        for key in kwargs.keys():
            self.__dict__['__{}'.format(key)] = kwargs.get(key)


# for ease of importing
from .drive import File, Permission
from .sheets import Spreadsheet, Sheet, Block
