from . import GoogleObject
from ..utils import keys_to_snake, keys_to_camel

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
        self._client = client
        self._new_permissions = []
        self._updates = []

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)


    @classmethod
    def from_existing(cls, client, data):
        """initiates existing permissions object"""

        new_data = keys_to_snake(data)
        return cls(client, **new_data)

    @property
    def id(self):
        return self._id

    @property
    def copy(self, name=None, parents=[]):
        """Copies self, optionally altering
        name and parent folders.
        """

        new = self.as_dict()
        new['name'] = name or '{0} | COPY'.format(self.name)
        new['parents'] = parents or self.parents

        return self.client.copy_file(self.id, new)


    def list_permissions(self):
        """returns list of permission for this
        drive file, return empty if caller is
        not authorized to share
        """

        permissions = []

        for permission in self._permissions:
            permissions.append(Permission(file=self, **permission))

        return permissions


    def create_permission(self, **kwargs):
        """initializes new permission objects and
        pushes it, returns
        and adds it
        to queue
        """

        if not kwargs.get('email'):
            raise ValueError

        permission = Permission(self, **kwargs)

        self._client.create_permission(
            file_id=self.id,
            permission=permission.as_dict()
        )

        return permission


class Permission(GoogleObject):

    """Google Drive File Permission"""

    _role_default = 'reader'
    _role_levels = {'reader', 'commenter', 'writer', 'owner'}

    _type_default = 'user'
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

        self._file = file

        self.email = kwargs.pop('email')
        self.role = kwargs.pop('role', self._role_default)
        self.type = kwargs.pop('type', self._type_default)

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, file, data):
        """initiates existing permissions object"""

        new_data = keys_to_snake(data)
        return cls(file, **new_data)

    @property
    def id(self):
        return self.__id

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        if value in self._role_levels:
            self._role = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value in self._type_levels:
            self.__type = value

    @property
    def email(self):
        return self.__email_address

    @email.setter
    def email(self, value):
    # TODO:
    #     add update call if _id is present
        self.__email_address = value

    def as_dict(self):
        """convert __dict__ keys to camel case, get
        intersection of this and _properties
        """

        return_dict = keys_to_camel(self.__dict__)
        keys = return_dict.keys()
        print keys
        key_set = set(keys)

        excess_key_set = key_set - self._properties
        print excess_key_set
        print return_dict
        excess_keys = list(excess_key_set)

        for key in excess_keys:
            del return_dict[key]

        return return_dict
