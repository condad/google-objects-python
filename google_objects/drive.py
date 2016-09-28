import re
import logging
from .utils import SlidesUpdate


class File(object):

    """Represents a Google Drive File object,
    is updatable
    """

    _types = {
        'application/vnd.google-apps.audio',
        'application/vnd.google-apps.document',
        'application/vnd.google-apps.drawing',
        'application/vnd.google-apps.file',
        'application/vnd.google-apps.folder',
        'application/vnd.google-apps.form',
        'application/vnd.google-apps.fusiontable',
        'application/vnd.google-apps.map',
        'application/vnd.google-apps.photo',
        'application/vnd.google-apps.presentation',
        'application/vnd.google-apps.script',
        'application/vnd.google-apps.sites',
        'application/vnd.google-apps.spreadsheet',
        'application/vnd.google-apps.unknown',
        'application/vnd.google-apps.video',
    }

    def __init__(self, data=None, client=None, type=None):
        """Initialize File Object

        :data: <Dict> of file data
        :client: <DriveAPI>

        """
        self._data = data
        self._permissions = None
        self._type = None

        self.client = client
        self.id = None
        self.name = None

        if data:
            self.id = data.get('id')
            self.name = data.get('name')
            self._permissions = data.get('permissions')
            self._type = data.get('mimeType')


    def __enter__(self):
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        # TODO:
        #     use .create for all new_permissions
        #     use .update for all old_permissions
        pass



    def permissions(self):
        """Permission Generator"""

        for each in self._permissions:
            yield Permission(each, self)

    def



class Permission(object):

    """Represents a Google Drive File Permission"""

    _permission_levels = {'reader', 'commenter', 'writer', 'admin'}

    def __init__(self, data=None,
            file=None, email=None, role='reader'):

        """Initialize Permission Object

        :data: <Dict> of Permission file data
        :level: one of reader, commenter, writer, or owner

        """

        if role not in self._permission_levels:
            raise ValueError

        self._data = data
        self._level = role
