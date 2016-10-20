# -*- coding: utf-8 -*-

import httplib2

from apiclient import discovery
from apiclient.errors import HttpError


class GoogleAPI(object):

    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """
    def __init__(self, credentials):
        self._credentials = credentials

    def build(self, service, version, discovery_url=None):
        """create api specific http resource"""

        http = self._credentials.authorize(httplib2.Http())
        # return discovery.build(service, version, http=http, discoveryServiceUrl=discovery_url)
        return discovery.build(service, version, http=http)

    def get_permissions(self, api):
        pass


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resources.
    """

    def __init__(self, **kwargs):
        # initalize  properties
        for key, val in kwargs.iteritems():
            setattr(self, '_{}'.format(key), val)
            # self.__dict__['_{}'.format(key)] = val


# for ease of importing
from .drive import DriveAPI
from .sheets import SheetsAPI
# confidential
from .slides import SlidesAPI
