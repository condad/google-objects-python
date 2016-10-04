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

    def list_files(self, type=None, fields=['files(id, name)']):
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """

        if hasattr(fields, '__iter__'):
            fields = ', '.join(fields)

        files = self._resource.files()
        files.list(
            q='mimeType=\'{}\''.format(type.lower()),
            pageSize=100,
            fields=fields
        )
        files.execute()

        return [File.from_existing(each, self) for each in files]


    def create_permission(self, file_id, permission, message=None, notification=False):
        # makes api call
        data = self._resource.permissions().create(
            fileId=file_id,
            body=permission,
            emailMessage=message,
            sendNotificationEmail=notification,
        ).execute()

        return Permission(**data)


class SheetsAPI(GoogleAPI):

    """Creates a Google Sheets Resource"""

    def __init__(self, credentials):
        """Google Drive API client, exposes
        collection resources
        """
        super(self.__class__, self).__init__(credentials)
        self._resource = self.build('sheets', 'v4')

    def get_spreadsheet(self, id):
        """Returns a Spreadsheet Object

        :id: Spreadsheet ID
        :returns: <Spreadsheet> Model

        """
        data = self._resource.spreadsheets().get(
            spreadsheetId=id
        ).execute()

        return Spreadsheet.from_existing(data, self)


    def get_values(self, spreadsheet_id, range_name):
        """Initialize a new block and return it"""

        data = self._resource.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        return Block.from_existing(data, client=self)

    def push_updates(self, spreadsheet_id, updates):
        spreadsheets = self._resource.spreadsheets()
        spreadsheets.batchUpdate(
            presentationId = spreadsheet_id,
            body={'requests': updates}
        )
        spreadsheets.execute()
