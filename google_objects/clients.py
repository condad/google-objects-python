# -*- coding: utf-8 -*-

"""

Google Slides API HTTP Resources,
classes in this file raise Exceptions.

    Tue 13 Sep 22:17:15 2016

"""

import os
import re
import logging
import httplib2

from apiclient import discovery
from apiclient.errors import HttpError

from .drive import File, Permission
from .sheets import Spreadsheet, Block


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO:
#     i/ type match credentials
#     ii/ start exception handling



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


class DriveAPI(GoogleAPI):

    """Google Drive Wrapper Object,
    exposes all Drive API operations
    """

    def __init__(self, credentials):
        """Google Drive API client, exposes
        collection resources
        """
        super(self.__class__, self).__init__(credentials)
        self._resource = self.build('drive', 'v3')

    def get_file(self, file_id):
        """Returns an initialized
        File Instance.

        :file_id: Google Drive File ID
        :returns: <File>

        """

        data = self._resource.files().get(
            fileId=file_id
        ).execute()

        return File.from_existing(self, data)

    def copy_file(self, file_id, file_body):
        """Copy file and place in folder.

        :file_id: drive file id
        :folder_id: drive file#folder id
        :returns: new, copied <File>

        """
        parents = file_body.get('parents')
        name = file_body.get('name')
        # get old file metadata if none provided
        if not parents or name:
            old_file = self._resource.files()
            old_file.get(fileId = file_id)
            old_file.execute()

            if not parents:
                parents = old_file.get('parents')
            if not name:
                name = '{0} | COPY'.format(old_file.get('name'))

        # set metadata body
        metadata = {'name': name, 'parents': parents}

        new_file = self._resource.files()
        new_file.copy(
            fileId=file_id,
            body=file_body,
            fields='id, webViewLink'
        )
        new_file.execute()

        return File(new_file, client=self)

    def list_files(self, type=None, fields=[]):
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """

        fields = fields.join(', ')

        files = self._resource.files()
        files.list(
            q='mimeType=\'{}\''.format(type.lower()),
            pageSize=100,
            fields="files(id, name)"
        )
        files.execute()

        return [File(file, self) for file in files]


    def create_permission(self, file_id, permission, message=None, notification=False):
        # makes api call
        permissions = self._resource.permissions().create(
            fileId=file_id,
            body=permission,
            emailMessage=message,
            sendNotificationEmail=notification,
        ).execute()

        return permissions


class SheetsAPI(GoogleAPI):

    """Creates a Google Sheets Resource"""

    def __init__(self, credentials, **kwargs):
        super(self.__class__, self).__init__(credentials, **kwargs)
        base_url = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')

        self._resource = self.build('sheets', 'v4', discovery_url=base_url)


    def get_spreadsheet(self, id):
        """Returns a Spreadsheet Object

        :id: Spreadsheet ID
        :returns: <Spreadsheet> Model

        """
        data = self._resource.spreadsheets()
        data.get(spreadsheetId = id)
        data.execute()

        return Spreadsheet(self, data)


    def get_values(self, spreadsheet_id, range_name):
        """Initialize a new block and return it"""

        values = self._resource.spreadsheets().values()
        values.get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        )
        values.execute()

        return Block(self, values)

    def push_updates(self, spreadsheet_id, updates):
        spreadsheets = self._resource.spreadsheets()
        spreadsheets.batchUpdate(
            presentationId = spreadsheet_id,
            body={'requests': updates}
        )
        spreadsheets.execute()
