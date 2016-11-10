# -*- coding: utf-8 -*-

import httplib2

from apiclient import discovery
from apiclient.errors import HttpError

from .utils import set_private_attrs, keys_to_snake


class GoogleAPI(object):

    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """
    def __init__(self, credentials):
        self._credentials = credentials

    def build(self, service, version, **kwargs):
        """create api specific http resource"""

        http = self._credentials.authorize(httplib2.Http())
        return discovery.build(service, version, http=http, **kwargs)



class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resource
    values.
    """

    def __init__(self, **kwargs):
        """Set Resource corresponding **kwargs
        to private attributes.
        """
        set_private_attrs(self, kwargs)


    @classmethod
    def from_existing(cls, data, *args):
        new_data = keys_to_snake(data)
        return cls(*args, **new_data)



# for ease of importing
from .drive import DriveAPI
from .sheets import SheetsAPI
# confidential
from .slides import SlidesAPI
