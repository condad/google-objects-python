from . import GoogleObject
from .utils import keys_to_snake, keys_to_camel

"""
    Google Drive API Resource Objects.

        i/ File
        ii/ Permission

            Fri 30 Sep 00:52:13 2016
"""

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
    def type(self):
        return self._mime_type

    @type.setter
    def type(self, value):
        """ensures type is valid, assigns type to
        unknown if no argument is given"""

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

        new = self.as_dict()
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
