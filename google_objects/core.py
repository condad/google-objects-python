# -*- coding: utf-8 -*-

import os
import logging

from apiclient import discovery

from google_objects.auth import service_account_creds

log = logging.getLogger(__name__)


ENV_API_KEY = 'GOOGLE_API_KEY'
ENV_SERVICE_ACCOUNT = 'GOOGLE_SERVICE_ACCOUNT_PATH'
ENV_DELEGATED_USER = 'GOOGLE_DELEGATED_USER'


class GoogleClient(object):

    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """

    service = None
    version = None
    scope = {}

    def __init__(self, resource=None):
        self.resource = resource

    @classmethod
    def from_api_key(cls, api_key=None):
        """Authorizes a client from an Api Key."""

        api_key = api_key or os.getenv(ENV_API_KEY)

        if not api_key:
            raise ValueError('API Key not provided.')

        resource = discovery.build(cls.service, cls.version, developerKey=api_key)
        return cls(resource)

    @classmethod
    def from_service_account(cls, creds_path=None, user=None):
        """Authorizes a client from an Service Account Credential File."""

        creds_path = creds_path or os.getenv(ENV_SERVICE_ACCOUNT)
        user = user or os.getenv(ENV_DELEGATED_USER)

        if not creds_path:
            raise ValueError('Service Account path not provided.')

        http_client = service_account_creds(creds_path, user, scope=cls.scope)
        resource = discovery.build(cls.service, cls.version, http=http_client)
        return cls(resource)


class GoogleObject(object):

    """Sets private properties on subclasses,
    corresponding one-to-one with Google API Resource
    values.
    """

    def __init__(self, *args, **kwargs):
        """Set Resource corresponding **kwargs
        to private attributes.
        """
        self.data = kwargs

    @classmethod
    def from_existing(cls, data, *args):
        return cls(*args, **data)

    def serialize(self):
        """convert __dict__ keys to camel case, get
        intersection of this and _properties
        """
        return self.data
