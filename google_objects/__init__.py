# -*- coding: utf-8 -*-

import os
import logging
import httplib2

from apiclient import discovery

from .utils import set_private_attrs
from .utils import keys_to_snake, keys_to_camel


# sets default logging handler to avoid "No handler found" warnings.
try:
    # for Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

SCOPES = {
    'drive',
    'spreadsheets'
}


def _gen_scopes(scopes):
    return ['https://www.googleapis.com/auth/' + each for each in scopes]


class GoogleAPI(object):

    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """

    def __init__(self, credentials=None, api_key=None):
        self.credentials = credentials
        self.api_key = api_key

    def build(self, service, version, **kwargs):
        """Create an API specific HTTP resource."""

        if self.api_key:
            return discovery.build(service, version,
                                   developerKey=self.api_key, **kwargs)

        http = self.credentials.authorize(httplib2.Http())
        return discovery.build(service, version, http=http, **kwargs)

    @classmethod
    def from_service_account(cls, creds_path, scope=SCOPES, user=None):
        from oauth2client.service_account import ServiceAccountCredentials as S

        creds_path = os.path.expanduser(creds_path)
        creds = S.from_json_keyfile_name(creds_path, _gen_scopes(scope))
        if user:
            creds = creds.create_delegated(user)

        return cls(creds)


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resource
    values.
    """

    _properties = set()

    def __init__(self, **kwargs):
        """Set Resource corresponding **kwargs
        to private attributes.
        """
        set_private_attrs(self, kwargs)

    @classmethod
    def from_existing(cls, data, *args):
        new_data = keys_to_snake(data)
        return cls(*args, **new_data)

    def serialize(self):
        """convert __dict__ keys to camel case, get
        intersection of this and _properties
        """

        return_dict = keys_to_camel(vars(self))
        keys = return_dict.keys()

        # return only defined properties
        excess_keys = set(keys) - self._properties
        for key in excess_keys:
            del return_dict[key]

        return return_dict


from .drive import DriveAPI
from .sheets import SheetsAPI
from .slides import SlidesAPI
