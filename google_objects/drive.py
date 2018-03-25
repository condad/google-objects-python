# -*- coding: utf-8 -*-

"""

Google Drive API
    Tue 13 Sep 22:16:41 2016

"""

import uuid
import logging

from google_objects.core import GoogleClient
from google_objects.core import GoogleObject

log = logging.getLogger(__name__)


class DriveClient(GoogleClient):

    """Google Drive Wrapper Object,
    exposes all Drive API operations.

    callback: receving webook URL.
    """

    service = 'drive'
    version = 'v3'
    scope = {'drive'}

    def get_about(self, fields=['user']):
        data = self.resource.about().get(
            fields=', '.join(fields)
        ).execute()

        return About.from_existing(data)

    def get_file(self, file_id):
        """Returns an initialized
        File Instance.

        :file_id: Google Drive File ID
        :returns: <File>

        """

        data = self.resource.files().get(
            fileId=file_id
        ).execute()

        return File.from_existing(data, self)

    def copy_file(self, file_id, file_body=None):
        """Copy file and place in folder.

        :file_id: drive file id
        :folder_id: drive file#folder id
        :returns: new, copied <File>

        """

        # get old file metadata if none provided
        if not file_body:
            file_body = self.resource.files().get(
                fileId=file_id
            ).execute()

        new_file = self.resource.files().copy(
            fileId=file_id,
            body=file_body,
            fields='id, webViewLink'
        ).execute()

        return File.from_existing(new_file, self)

    def list_files(self, file_type=None,
                   parents=[], fields=['files(id, name)']):
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """

        if hasattr(fields, '__iter__'):
            fields = ', '.join(fields)

        query = ''
        if file_type:
            prfx = 'application/vnd.google-apps.'
            query = query + "mimeType='{}'".format('application/vnd.google-apps.' + file_type.lower())
        for p in parents:
            query = query + ' and \'{}\' in parents'.format(p)

        result = self.resource.files().list(
            q=query, pageSize=100,  # fields=fields
        ).execute()

        files = result.get('files')

        return [File.from_existing(each, self) for each in files]

    def watch_file(self, file_id,
                   channel_id=None, callback=None, type='webhook'):
        """Commences push notifications for a file resource,
        depends on callback url being set on instance.

        :file_id: Google Drive File Resource ID
        :returns:

        """
        if not (callback or self.callback):
            raise ValueError('Callback URL required to watch resources.')

        req_body = {
            'id': channel_id or str(uuid.uuid4()),
            'type': type,
            'address': callback or self.callback
        }
        resp = self.resource.files().watch(
            fileId=file_id, body=req_body
        ).execute()

        return resp

    def create_permission(self, file_id,
                          permission, message=None, notification=True):
        # makes api call
        data = self.resource.permissions().create(
            fileId=file_id,
            body=permission,
            emailMessage=message,
            sendNotificationEmail=notification,
        ).execute()

        return Permission(**data)


class About(GoogleObject):

    """Docstring for User Resource, this is READ ONLY"""

    @property
    def user(self):
        return self.data['user']

    @property
    def email(self):
        return self.user['emailAddress']

    @property
    def name(self):
        return self.user['displayName']

    @property
    def photo(self):
        return self.user['photoLink']

    @property
    def permission_id(self):
        return self.user['permissionId']


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
        :client: <DriveClient>

        """
        self.client = client
        self.__new_permissions = []
        self.__updates = []

        # initalize the other properties
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.data['id'] or None

    @property
    def name(self):
        return self.data['name'] or None

    @name.setter
    def name(self, val):
        self.data['name'] = val

    @property
    def url(self):
        return self.data['webViewLink']

    @property
    def type_prefix(self):
        return self.data['typePrefix']

    @property
    def type(self):
        return self.data['mimeType']

    @type.setter
    def type(self, value):
        """ensures type is valid, assigns type to
        unknown if no argument is given
        """

        file_type = value or self._default_type
        file_type = value.lower()
        if value not in self._types:
            raise ValueError

        self.data['mimeType'] = '{}{}'.format(self.type_prefix, file_type)

    @property
    def parents(self):
        return self.data['parents']

    @parents.setter
    def parents(self, value):
        self.data['parents'] = value

    def copy(self, name=None, parents=[]):
        """Copies self, optionally altering
        name and parent folders.
        """

        new = dict()
        new['name'] = name or '{0} | COPY'.format(self.name)
        if parents:
            new['parents'] = parents

        return self.client.copy_file(self.id, new)

    def permissions(self):
        return [Permission(self, **each) for each in self.data['permissions']]

    def add_permission(self, email, **kwargs):
        """initializes new permission objects and
        pushes it, returns
        and adds it
        to queue
        """

        kwargs.update({'email': email, 'emailAddress': email})
        permission = Permission.from_existing(kwargs, self)
        message = kwargs.get('message')
        notification = kwargs.get('notification')

        created = self.client.create_permission(
            self.id, permission.serialize(), message, notification
        )

        created.file = self
        created.email = email

        return created

    def watch(self, **kwargs):
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
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.data['id']

    @property
    def role(self):
        return self.data.get('role', self._default_role)

    @role.setter
    def role(self, value):
        if value in self._role_levels:
            self.data['role'] = value

    @property
    def type(self):
        return self.data.get('type', self._default_type)

    @type.setter
    def type(self, value):
        if value in self._type_levels:
            self.data['type'] = value

    @property
    def email(self):
        return self.data['emailAddress']

    @email.setter
    def email(self, value):
        # TODO:
        #     add update call if _id is present
        if len(value.split('@')) is 2:
            self.data['emailAddress'] = value
