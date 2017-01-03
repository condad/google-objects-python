# -*- coding: utf-8 -*-

"""

Google Drive API
    Tue 13 Sep 22:16:41 2016

"""

import uuid
import logging

from . import GoogleAPI, GoogleObject
from .utils import keys_to_snake, keys_to_camel

log = logging.getLogger(__name__)


# TODO:
    # i/ add greater permissions functionality
    # ii/ change .from_existing to .from_raw
    # add SKELETON to set attributes to null when not set


class DriveAPI(GoogleAPI):

    """Google Drive Wrapper Object,
    exposes all Drive API operations.

    callback: receving webook URL.
    """

    def __init__(self, credentials, callback=None):
        """Google Drive API cliSpirited Awayent, exposes
        collection resources
        """
        super(self.__class__, self).__init__(credentials)
        self._resource = self.build('drive', 'v3')
        self.callback = callback

    def get_about(self, fields=['user']):
        data = self._resource.about().get(
            fields=', '.join(fields)
        ).execute()

        return About.from_existing(data)

    def get_file(self, file_id):
        """Returns an initialized
        File Instance.

        :file_id: Google Drive File ID
        :returns: <File>

        """

        data = self._resource.files().get(
            fileId=file_id
        ).execute()

        return File.from_existing(data, self)

    def copy_file(self, file_id, file_body):
        """Copy file and place in folder.

        :file_id: drive file id
        :folder_id: drive file#folder id
        :returns: new, copied <File>

        """

        # get old file metadata if none provided
        if not file_body:
            file_body = self._resource.files().get(
                fileId=file_id
            ).execute()

        new_file = self._resource.files().copy(
            fileId=file_id,
            body=file_body,
            fields='id, webViewLink'
        ).execute()

        return File.from_existing(new_file, self)

    def list_files(self, file_type=None, parents=[], fields=['files(id, name)']):
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """

        if hasattr(fields, '__iter__'):
            fields = ', '.join(fields)

        query = ''
        if file_type:
            query = query + "mimeType='{}'".format('application/vnd.google-apps.' + file_type.lower())
        for p in parents:
            query = query + ' and \'{}\' in parents'.format(p)

        result = self._resource.files().list(
            q=query,
            pageSize=100,
            # fields=fields
        ).execute()

        files = result.get('files')

        return [File.from_existing(each, self) for each in files]

    def watch_file(self, file_id, channel_id=str(uuid.uuid4()), callback=None, type='webhook'):
        """Commences push notifications for a file resource,
        depends on callback url being set on instance.

        :file_id: Google Drive File Resource ID
        :returns:

        """
        if not (callback or self.callback):
            raise ValueError('Callback URL required to watch resources.')

        req_body = {
            'id': channel_id,
            'type': type,
            'address': callback or self.callback
        }
        result = self._resource.files().watch(
            fileId=file_id,
            body=req_body
        ).execute()

        return keys_to_snake(result)

    def create_permission(self, file_id, permission, message=None, notification=False):
        # makes api call
        data = self._resource.permissions().create(
            fileId=file_id,
            body=permission,
            emailMessage=message,
            sendNotificationEmail=notification,
        ).execute()

        return Permission(**data)



# objects


class About(GoogleObject):

    """Docstring for User Resource, this is READ ONLY"""

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    @property
    def email(self):
        return self._user['email_address']

    @property
    def name(self):
        return self._user['display_name']

    @property
    def photo(self):
        return self._user['photo_link']

    @property
    def permission_id(self):
        return self._user['permission_id']


class File(GoogleObject):

    """Represents a Google Drive File Resource"""

    _type_prefix = 'application/vnd.google-apps.'

    # drive file types
    _default_type = 'unknown'
    _types = {
        'audio',
        'document',
        'drawing',
        'file',
        'folder',
        'form',
        'fusiontable',
        'map',
        'photo',
        'presentation',
        'script',
        'sites',
        'spreadsheet',
        'unknown',
        'video',
    }

    def __init__(self, client=None, **kwargs):
        """Initialize File Object

        :data: <Dict> of file data
        :client: <DriveAPI>

        """
        self.client = client
        self.__new_permissions = []
        self.__updates = []

        self.type = kwargs.pop('type', self._default_type)
        self.parents = kwargs.pop('parents', [])

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, data, client):
        """initiates existing permissions object"""

        new_data = keys_to_snake(data)
        return cls(client, **new_data)

    @property
    def id(self):
        return self._id or None

    @property
    def name(self):
        return self._name or None

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def type(self):
        return self._mime_type

    @type.setter
    def type(self, value):
        """ensures type is valid, assigns type to
        unknown if no argument is given
        """

        file_type = value or self._default_type
        file_type = value.lower()
        if value not in self._types:
            raise ValueError

        self._mime_type = '{}{}'.format(self._type_prefix, file_type)

    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, value):
        self._parents = value

    def copy(self, name=None, parents=[]):
        """Copies self, optionally altering
        name and parent folders.
        """

        new = dict()
        new['name'] = name or '{0} | COPY'.format(self.name)
        if parents:
            new['parents'] = parents

        return self.client.copy_file(self.id, new)

    def list_permissions(self):
        """returns list of permission for this
        drive file, return empty if caller is
        not authorized to share
        """

        permissions = []

        for permission in self._permissions:
            permissions.append(Permission(self, **permission))

        return permissions

    def add_permission(self, **kwargs):
        """initializes new permission objects and
        pushes it, returns
        and adds it
        to queue
        """

        if not 'email' in kwargs:
            raise ValueError

        permission = Permission.from_existing(kwargs, self)

        created = self.client.create_permission(
            file_id=self.id,
            permission=permission.as_dict()
        )

        created.file = self
        created.email = kwargs['email']

        return created

    def start_watching(self, **kwargs):
        """Attempts to start receiving push notifications for this file.

        :channel_id: UUID
        :returns: Dictionary detailing watch request.

        """
        return self.client.watch_file(self.id, **kwargs)


class Permission(GoogleObject):

    """Google Drive File Permission"""

    _default_role = 'reader'
    _role_levels = {'reader', 'commenter', 'writer', 'owner'}

    _default_type = 'user'
    _type_levels = {'user', 'group', 'domain', 'anyone'}

    # api key names
    _properties = {'role', 'type',
                   'emailAddress', 'allowFileDiscovery', 'domain'}

    # constructors

    def __init__(self, file=None, **kwargs):

        """Initialize Permission Object

        :data: <Dict> of Permission file data
        :level: one of reader, commenter, writer, or owner

        """

        self.file = file

        self.email = kwargs.get('email', '')
        self.role = kwargs.pop('role', self._default_role)
        self.type = kwargs.pop('type', self._default_type)

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, data, file):
        """initiates existing permissions object"""

        new_data = keys_to_snake(data)
        return cls(file, **new_data)

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value in self._role_levels:
            self._role = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in self._type_levels:
            self._type = value

    @property
    def email(self):
        return self._email_address

    @email.setter
    def email(self, value):
    # TODO:
    #     add update call if _id is present
        if len(value.split('@')) is 2:
            self._email_address = value

    def as_dict(self):
        """convert __dict__ keys to camel case, get
        intersection of this and _properties
        """

        return_dict = keys_to_camel(self.__dict__)
        keys = return_dict.keys()
        key_set = set(keys)

        excess_key_set = key_set - self._properties
        excess_keys = list(excess_key_set)

        for key in excess_keys:
            del return_dict[key]

        return return_dict
