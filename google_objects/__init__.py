# -*- coding: utf-8 -*-

import logging

from apiclient import discovery

from google_objects.auth import service_account_creds
from google_objects.utils import set_private_attrs
from google_objects.utils import keys_to_snake, keys_to_camel

# sets default logging handler to avoid "No handler found" warnings.
try:
    # for Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


class GoogleClient(object):

    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """

    def __init__(self, resource=None):
        self.resource = resource

    @classmethod
    def from_api_key(cls, service, version, api_key):
        """Authorizes a client from an Api Key."""

        if not api_key:
            raise ValueError('Please provide an API Key.')

        resource = discovery.build(service, version, developerKey=api_key)
        return cls(resource)

    @classmethod
    def from_service_account(cls, service, version,
                             creds_path=None, user=None, scope=[]):
        """Authorizes a client from an Service Account Credential File."""

        if not creds_path:
            err = 'Please provide an a path to your service credentals.'
            raise ValueError(err)

        http_client = service_account_creds(creds_path, user, scope=scope)
        resource = discovery.build(service, version, http=http_client)
        return cls(resource)


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resource
    values.
    """

    def __init__(self, **kwargs):
        """Set Resource corresponding **kwargs
        to private attributes.
        """
        self.data = keys_to_snake(kwargs)
        set_private_attrs(self, kwargs)

    @classmethod
    def from_existing(cls, data, *args):
        return cls(*args, **data)

    def serialize(self):
        """convert __dict__ keys to camel case, get
        intersection of this and _properties
        """
        return keys_to_camel(self.data)


from .drive.core import DriveClient
from .sheets.core import SheetsClient
from .slides.core import SlidesClient
