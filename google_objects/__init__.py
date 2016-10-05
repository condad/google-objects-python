# -*- coding: utf-8 -*-


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resources.
    """

    def __init__(self, **kwargs):
        # initalize  properties
        for key in kwargs.keys():
            self.__dict__['_{}'.format(key)] = kwargs.get(key)


# for ease of importing
from .clients import DriveAPI, SheetsAPI
from .drive import File, Permission
from .sheets import Spreadsheet, Sheet, Block

# confidential
from .slides import SlidesAPI, Presentation, Page
